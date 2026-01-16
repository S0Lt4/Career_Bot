from jinja2 import Template
import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kariyer Raporu - {{ user_name }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .result-card { background: #e8f6f3; border-left: 5px solid #1abc9c; padding: 20px; margin: 20px 0; }
        .result-title { font-size: 24px; font-weight: bold; color: #16a085; }
        .scores { display: flex; justify-content: space-around; margin: 30px 0; flex-wrap: wrap; }
        .score-box { text-align: center; background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); min-width: 100px; margin: 10px; }
        .score-val { font-size: 2em; font-weight: bold; color: #3498db; }
        .btn { display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px; }
        .btn:hover { background: #2980b9; }
        .footer { margin-top: 50px; font-size: 0.8em; color: #7f8c8d; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Kariyer Keşif Raporu</h1>
        <p>Merhaba <strong>{{ user_name }}</strong>, verdiğin cevaplara göre senin için en uygun kariyer yolunu analiz ettik.</p>
        
        <div class="result-card">
            <div>Senin için Önerilen Meslek:</div>
            <div class="result-title">{{ career_title }}</div>
            <p>{{ career_desc }}</p>
            <a href="{{ roadmap_url }}" class="btn" target="_blank">Yol Haritasını İncele</a>
        </div>

        <h3>Kişisel Puanların vs Meslek Gereksinimleri</h3>
        <div class="scores">
            <div class="score-box">
                <div>Analitik</div>
                <div class="score-val">{{ u_a }} / 10</div>
                <small>Meslek: {{ c_a }}</small>
            </div>
            <div class="score-box">
                <div>Sosyal</div>
                <div class="score-val">{{ u_s }} / 10</div>
                <small>Meslek: {{ c_s }}</small>
            </div>
            <div class="score-box">
                <div>Yaratıcılık</div>
                <div class="score-val">{{ u_y }} / 10</div>
                <small>Meslek: {{ c_y }}</small>
            </div>
        </div>

        <p>Bu rapor tamamen Python kullanılarak, senin cevaplarına özel olarak oluşturulmuştur.</p>
        
        <div class="footer">
            Career Bot Demo Tarafından Oluşturuldu - {{ date }}
        </div>
    </div>
</body>
</html>
"""

def generate_report(user_name, user_scores, matched_career):
    from datetime import datetime
    
    template = Template(HTML_TEMPLATE)
    
    html_content = template.render(
        user_name=user_name,
        career_title=matched_career['title'],
        career_desc=matched_career['description'],
        roadmap_url=matched_career['roadmap_url'],
        u_a=user_scores.get('analitik', 0),
        u_s=user_scores.get('sosyal', 0),
        u_y=user_scores.get('yaraticilik', 0),
        c_a=matched_career['score_analitik'],
        c_s=matched_career['score_sosyal'],
        c_y=matched_career['score_yaraticilik'],
        date=datetime.now().strftime("%d.%m.%Y")
    )
    
    filename = f"report_{user_name}_{datetime.now().strftime('%Y%m%d%H%M')}.html"
    filepath = os.path.join("reports", filename) # Save to reports folder if possible; ensure it exists
    
    os.makedirs("reports", exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return filepath
