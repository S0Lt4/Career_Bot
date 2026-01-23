
from modules.visualizer import CareerVisualizer
import os

def check_viz():
    viz = CareerVisualizer()
    
    # Mock Data
    username = "TestUser"
    career = {
        'title': 'Yazılım Geliştirici',
        'field': 'Teknoloji',
        'description': 'Test Description for Visualization.',
        'roadmap_url': 'https://roadmap.sh/full-stack',
        'score_analitik': 9,
        'score_sosyal': 4,
        'score_yaraticilik': 7
    }
    user_scores = {'analitik': 8, 'sosyal': 5, 'yaraticilik': 7}
    
    print("Generating Card...")
    path = viz.create_career_card(username, career, user_scores)
    
    if os.path.exists(path):
        print(f"PASS: Image generated at {path}")
    else:
        print("FAIL: Image not found.")

if __name__ == "__main__":
    check_viz()
