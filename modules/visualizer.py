
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.gridspec import GridSpec

class CareerVisualizer:
    def __init__(self):
        # Matplotlib style configuration for dark "Scientific" theme
        plt.style.use('dark_background')
        self.colors = {
            'bg': '#1a1a2e',
            'user': '#00d2fc',    # Neon Blue
            'career': '#ff005c',  # Neon Red/Pink
            'grid': '#323259',
            'text': '#e0e0e0'
        }

    def get_popularity_score(self, url):
        """
        Scrapes the roadmap URL to estimate popularity based on content length/links.
        Returns a score (0-100) and a label.
        """
        try:
            if not url or "http" not in url:
                return 50, "Bilinmiyor"
            
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code != 200:
                return 50, "Veri Alınamadı"

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Simple heuristic
            links = len(soup.find_all('a'))
            lists = len(soup.find_all('li'))
            density = links + lists
            
            # Normalize: Assume 500+ items is "Very Popular" (100 pts)
            score = min(100, int((density / 500) * 100))
            
            if score > 80: label = "Çok Popüler"
            elif score > 50: label = "Popüler"
            elif score > 20: label = "Gelişmekte"
            else: label = "Niş Alan"
            
            return score, label

        except Exception as e:
            print(f"Scraping error: {e}")
            return 50, "Hata"

    def create_career_card(self, username, career, user_scores):
        """
        Generates a High-Quality Scientific Plot image card.
        """
        # Create figure and grid layout
        fig = plt.figure(figsize=(10, 6), facecolor=self.colors['bg'])
        gs = GridSpec(2, 2, width_ratios=[1.5, 1], height_ratios=[4, 1])
        
        # --- 1. RADAR CHART (Main Plot) ---
        categories = ['Analitik', 'Sosyal', 'Yaratıcılık']
        N = len(categories)
        
        # Compute angles
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1] # Close the loop
        
        # Data Setup
        user_values = [
            user_scores.get('analitik', 0),
            user_scores.get('sosyal', 0),
            user_scores.get('yaraticilik', 0)
        ]
        user_values += user_values[:1] # Close loop
        
        career_values = [
            career['score_analitik'],
            career['score_sosyal'],
            career['score_yaraticilik']
        ]
        career_values += career_values[:1] # Close loop
        
        # Polar Plot
        ax = fig.add_subplot(gs[:, 0], polar=True, facecolor=self.colors['bg'])
        
        # Draw User Poly
        ax.plot(angles, user_values, color=self.colors['user'], linewidth=2, linestyle='solid', label=username)
        ax.fill(angles, user_values, color=self.colors['user'], alpha=0.25)
        
        # Draw Career Poly
        ax.plot(angles, career_values, color=self.colors['career'], linewidth=2, linestyle='dashed', label=career['title'])
        ax.fill(angles, career_values, color=self.colors['career'], alpha=0.1)
        
        # Fix Axis Labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12, color='white', weight='bold')
        
        # Y-Labels (0-10)
        ax.set_rlabel_position(0)
        plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#aaaaaa", size=8)
        plt.ylim(0, 10)
        
        # Customize Grid
        ax.grid(color=self.colors['grid'], linewidth=1, linestyle='--')
        ax.spines['polar'].set_visible(False) # Hide outer circle line
        
        # Legend (Top Left)
        plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1.1), frameon=False, labelcolor='white')

        # --- 2. TEXT INFO (Top Right) ---
        ax_text = fig.add_subplot(gs[0, 1])
        ax_text.axis('off')
        
        info_text = (
            f"KARİYER ANALİZİ\n"
            f"----------------\n"
            f"ADAY: {username}\n"
            f"MESLEK: {career['title']}\n"
            f"ALAN: {career['field']}\n\n"
            f"UYUM PUANLARI:\n"
            f"A: {user_scores.get('analitik',0)} / {career['score_analitik']}\n"
            f"S: {user_scores.get('sosyal',0)} / {career['score_sosyal']}\n"
            f"Y: {user_scores.get('yaraticilik',0)} / {career['score_yaraticilik']}\n"
        )
        
        ax_text.text(0, 0.9, info_text, color='white', fontsize=11, family='monospace', verticalalignment='top')
        
        # Description
        desc = career['description']
        if len(desc) > 80: desc = desc[:80] + "..."
        ax_text.text(0, 0.3, f"TANIM:\n{desc}", color='#aaaaaa', fontsize=9, wrap=True, verticalalignment='top')

        # --- 3. POPULARITY METER (Bottom Right) ---
        pop_score, pop_label = self.get_popularity_score(career['roadmap_url'])
        
        ax_pop = fig.add_subplot(gs[1, 1])
        ax_pop.set_facecolor(self.colors['bg'])
        
        # Draw a scientific-looking gauge bar
        # Gradient effect simulated with bars
        ax_pop.barh([0], [100], color='#333333', height=0.5) # Background
        
        # Color based on score
        if pop_score > 80: pop_c = '#00ff00' # Green
        elif pop_score > 50: pop_c = '#ffff00' # Yellow
        else: pop_c = '#ff0000' # Red
            
        ax_pop.barh([0], [pop_score], color=pop_c, height=0.5)
        
        ax_pop.set_xlim(0, 100)
        ax_pop.set_ylim(-0.5, 0.5)
        ax_pop.axis('off')
        
        # Label above bar
        ax_pop.text(0, 0.6, f"POPÜLARİTE ENDEKSİ: {pop_score}/100", color=pop_c, fontsize=10, weight='bold')
        ax_pop.text(100, 0.6, pop_label, color='white', fontsize=9, ha='right')
        
        # --- SAVE ---
        os.makedirs("reports", exist_ok=True)
        output_path = f"reports/card_{username}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor=self.colors['bg'])
        plt.close(fig) # Close to free memory
        
        return output_path
