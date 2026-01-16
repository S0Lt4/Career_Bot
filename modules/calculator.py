import math

def calculate_best_career(user_scores, all_careers):
    """
    Kullanıcı puanları ile meslek puanları arasındaki en yakın eşleşmeyi bulur.
    Öklid mesafesi (Euclidean distance) yöntemi kullanılmıştır.
    """
    # user_scores: {'analitik': 5, 'sosyal': 3, 'yaraticilik': 8}
    # all_careers: List of dicts from DB
    
    best_match = None
    min_distance = float('inf')
    
    u_a = user_scores.get('analitik', 0)
    u_s = user_scores.get('sosyal', 0)
    u_y = user_scores.get('yaraticilik', 0)
    
    for career in all_careers:
        c_a = career['score_analitik']
        c_s = career['score_sosyal']
        c_y = career['score_yaraticilik']
        
        # 3 boyutlu uzayda mesafe hesapla
        distance = math.sqrt(
            (u_a - c_a) ** 2 +
            (u_s - c_s) ** 2 +
            (u_y - c_y) ** 2
        )
        
        if distance < min_distance:
            min_distance = distance
            best_match = career
            
    return best_match
