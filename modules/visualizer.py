
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import os

class CareerVisualizer:
    def __init__(self):
        self.font_path = "arial.ttf" # Windows default
        try:
            self.title_font = ImageFont.truetype(self.font_path, 40)
            self.text_font = ImageFont.truetype(self.font_path, 20)
            self.small_font = ImageFont.truetype(self.font_path, 15)
        except:
            self.title_font = ImageFont.load_default()
            self.text_font = ImageFont.load_default()
            self.small_font = ImageFont.load_default()

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
            
            # Simple heuristic: Count links and lists as a proxy for "Resource Density"
            links = len(soup.find_all('a'))
            lists = len(soup.find_all('li'))
            density = links + lists
            
            # Normalize: Assume 500+ items is "Very Popular" (100 pts)
            score = min(100, int((density / 500) * 100))
            
            if score > 80: label = "Çok Popüler 🔥"
            elif score > 50: label = "Popüler ⭐"
            elif score > 20: label = "Gelişmekte 📈"
            else: label = "Niş Alan 🎯"
            
            return score, label

        except Exception as e:
            print(f"Scraping error: {e}")
            return 50, "Hata"

    def create_career_card(self, username, career, user_scores):
        """
        Generates a PNG image card.
        """
        width, height = 800, 400
        background_color = (30, 30, 45) # Dark Blue/Grey
        text_color = (255, 255, 255)
        accent_color = (52, 152, 219) # Blue
        
        image = Image.new('RGB', (width, height), background_color)
        draw = ImageDraw.Draw(image)
        
        # 1. Title
        draw.text((30, 30), f"Kariyer Önerisi: {career['title']}", font=self.title_font, fill=text_color)
        draw.text((30, 80), f"Kullanıcı: {username}", font=self.text_font, fill=(200, 200, 200))
        
        # 2. Field & Description
        draw.text((30, 120), f"Alan: {career['field']}", font=self.text_font, fill=accent_color)
        
        # Wrap description
        desc = career['description']
        # Simple wrapping logic for visualization (truncate if too long)
        if len(desc) > 60: desc = desc[:60] + "..."
        draw.text((30, 150), desc, font=self.text_font, fill=text_color)
        
        # 3. Popularity Section
        pop_score, pop_label = self.get_popularity_score(career['roadmap_url'])
        
        draw.text((30, 220), "Kariyer Ekosistem Popülaritesi:", font=self.text_font, fill=(255, 204, 0))
        
        # Draw Bar Background
        bar_x, bar_y, bar_w, bar_h = 30, 250, 400, 30
        draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=(50, 50, 60))
        
        # Draw Progress
        fill_w = int(bar_w * (pop_score / 100))
        draw.rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], fill=(46, 204, 113))
        
        draw.text((bar_x + fill_w + 10, bar_y + 5), f"{pop_score}/100 ({pop_label})", font=self.small_font, fill=text_color)
        
        # 4. Save
        output_path = f"reports/card_{username}.png"
        image.save(output_path)
        return output_path
