import math

def calculate_distance(user_scores, career):
    """Kullanıcı ve meslek arasındaki Öklid mesafesini hesaplar."""
    u_a = user_scores.get('analitik', 0)
    u_s = user_scores.get('sosyal', 0)
    u_y = user_scores.get('yaraticilik', 0)
    
    c_a = career['score_analitik']
    c_s = career['score_sosyal']
    c_y = career['score_yaraticilik']
    
    return math.sqrt(
        (u_a - c_a) ** 2 +
        (u_s - c_s) ** 2 +
        (u_y - c_y) ** 2
    )

def distance_to_percentage(distance):
    """
    Mesafeyi yüzdeye çevirir.
    Maksimum mesafe: sqrt(10^2 + 10^2 + 10^2) = sqrt(300) ≈ 17.32
    """
    max_distance = math.sqrt(300)  # 3 boyutta maksimum mesafe (0-10 ölçeğinde)
    percentage = max(0, 100 - (distance / max_distance * 100))
    return round(percentage)

def calculate_best_career(user_scores, all_careers):
    """
    Kullanıcı puanları ile meslek puanları arasındaki en yakın eşleşmeyi bulur.
    Geriye dönük uyumluluk için sadece en iyi eşleşmeyi döndürür.
    """
    top_matches = calculate_top_careers(user_scores, all_careers, top_n=1)
    if top_matches:
        return top_matches[0]['career']
    return None

def calculate_top_careers(user_scores, all_careers, top_n=3):
    """
    Kullanıcı puanları ile meslek puanları arasındaki en iyi N eşleşmeyi bulur.
    Her eşleşme için uyumluluk yüzdesi hesaplar.
    
    Returns:
        List of dicts: [{'career': career_dict, 'match_percentage': 85}, ...]
    """
    matches = []
    
    for career in all_careers:
        distance = calculate_distance(user_scores, career)
        percentage = distance_to_percentage(distance)
        
        matches.append({
            'career': career,
            'match_percentage': percentage,
            'distance': distance
        })
    
    # Yüzdeye göre sırala (en yüksek önce)
    matches.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    # En iyi N tanesini döndür
    return matches[:top_n]
