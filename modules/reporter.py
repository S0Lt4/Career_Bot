from jinja2 import Template
import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kariyer Analizi - {{ user_name }}</title>
    <style>
        :root {
            /* Palette: Black, Deep Dark Blue/Purple, Coffee, White, Dark Red, Dark Yellow */
            --bg-color: #050510;       /* Very Dark Blue/Black */
            --card-bg: #121016;        /* Deep matte purple/black */
            --text-main: #e0e0e0;      /* White-ish */
            --text-muted: #a0a0a0;     /* Grey */
            
            --accent-purple: #7b4397;  /* Primary Purple */
            --accent-coffee: #3e2723;  /* Dark Coffee */
            --accent-blue: #1565c0;    /* Dark Blue */
            --accent-red: #c62828;     /* Dark Red */
            --accent-yellow: #f9a825;  /* Dark Yellow */
        }
        
        body { 
            font-family: 'Segoe UI', serif; /* Simple, elegant font */
            background-color: var(--bg-color); 
            color: var(--text-main); 
            margin: 0; 
            padding: 0;
            display: flex;
            justify-content: center;
            min-height: 100vh;
        }
        
        .container { 
            width: 100%;
            max-width: 800px; 
            margin: 40px 20px; 
            background: var(--card-bg); 
            padding: 40px; 
            border-radius: 8px; /* Simple corners */
            border: 1px solid #2a202e; /* Subtle border */
        }
        
        h1 { 
            color: var(--accent-purple); 
            font-size: 2.2rem; 
            margin-bottom: 0.5rem; 
            text-align: center;
            border-bottom: 2px solid var(--accent-coffee);
            padding-bottom: 15px;
        }
        
        .subtitle {
            text-align: center;
            color: var(--text-muted);
            margin-bottom: 3rem;
            font-style: italic;
        }
        
        .result-card { 
            background-color: #1a151e; /* Slightly lighter than card-bg */
            padding: 30px; 
            border-left: 5px solid var(--accent-purple);
            margin-bottom: 40px;
            text-align: center;
        }
        
        .result-label {
            color: var(--text-muted);
            font-size: 0.85rem;
            letter-spacing: 1px;
            margin-bottom: 10px;
            display: block;
        }
        
        .result-title { 
            font-size: 2.5rem; 
            font-weight: bold; 
            color: var(--text-main);
            margin: 0;
        }
        
        .result-desc {
            font-size: 1.1rem;
            line-height: 1.6;
            color: #d1d1d1;
            margin: 20px 0;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .btn { 
            display: inline-block; 
            background-color: var(--accent-coffee); 
            color: #fff; 
            font-weight: bold;
            padding: 12px 30px; 
            text-decoration: none; 
            border-radius: 4px; /* Simple button */
            margin-top: 10px;
            border: 1px solid #5d4037;
        }
        .btn:hover { 
            background-color: #4e342e; 
            border-color: #8d6e63;
        }
        
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px;
            margin-top: 40px;
        }
        
        .stat-box { 
            background: rgba(255,255,255,0.03); 
            padding: 20px; 
            text-align: center;
            border-radius: 4px;
        }
        
        /* Specific Colors for Stats */
        .stat-box.blue { border-top: 3px solid var(--accent-blue); }
        .stat-box.red { border-top: 3px solid var(--accent-red); }
        .stat-box.yellow { border-top: 3px solid var(--accent-yellow); }
        
        .stat-label {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        
        .stat-val { 
            font-size: 2.5rem; 
            font-weight: bold; 
            color: var(--text-main);
        }
        
        .stat-sub {
            font-size: 0.8rem;
            color: #757575; /* Dark grey */
            margin-top: 5px;
        }
        
        .footer { 
            margin-top: 60px; 
            border-top: 1px solid #333;
            padding-top: 20px;
            font-size: 0.8rem; 
            color: #666; 
            text-align: center; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Kariyer Raporu</h1>
        <p class="subtitle">Aday: <strong>{{ user_name }}</strong> | ID: #{{ date }}</p>
        
        <div class="result-card">
            <span class="result-label">Yapay Zeka Önerisi</span>
            <div class="result-title">{{ career_title }}</div>
            <p class="result-desc">{{ career_desc }}</p>
            <a href="{{ roadmap_url }}" class="btn" target="_blank">Yol Haritasını Görüntüle →</a>
        </div>

        <h3 style="text-align:center; color: var(--text-main); font-weight: normal; margin-bottom: 20px;">Yetkinlik Analizi</h3>
        <div class="stats-grid">
            <div class="stat-box blue">
                <div class="stat-label">ANALİTİK ZEKA</div>
                <div class="stat-val" style="color: #42a5f5;">{{ u_a }}<span style="font-size:1rem; opacity:0.5; color: #aaa;">/10</span></div>
                <div class="stat-sub">Hedef: {{ c_a }}</div>
            </div>
            <div class="stat-box red">
                <div class="stat-label">SOSYAL BECERİ</div>
                <div class="stat-val" style="color: #ef5350;">{{ u_s }}<span style="font-size:1rem; opacity:0.5; color: #aaa;">/10</span></div>
                <div class="stat-sub">Hedef: {{ c_s }}</div>
            </div>
            <div class="stat-box yellow">
                <div class="stat-label">YARATICILIK</div>
                <div class="stat-val" style="color: #fdd835;">{{ u_y }}<span style="font-size:1rem; opacity:0.5; color: #aaa;">/10</span></div>
                <div class="stat-sub">Hedef: {{ c_y }}</div>
            </div>
        </div>

        <div class="footer">
            Generated by CareerBot AI System • {{ date }}
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
