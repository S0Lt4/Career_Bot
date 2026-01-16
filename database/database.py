import sqlite3
import os

class CareerBotDB:
    def __init__(self, db_path="database/bot_data.db"):
        # Klasör yoksa oluşturur
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        # Meslekler Tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS careers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                field TEXT,
                score_analitik INTEGER,
                score_sosyal INTEGER,
                score_yaraticilik INTEGER,
                description TEXT,
                roadmap_url TEXT
            )
        ''')
        # Kullanıcılar Tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                u_analitik INTEGER DEFAULT 0,
                u_sosyal INTEGER DEFAULT 0,
                u_yaraticilik INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_sample_data(self):
        # Genişletilmiş Meslek Listesi (Toplam 30 Meslek)
        meslekler = [
            # Mevcutlar
            ('Yazılım Geliştirici', 'Teknoloji', 9, 4, 7, 'Karmaşık problemleri kodla çözer.', 'https://roadmap.sh/full-stack'),
            ('Grafik Tasarımcı', 'Sanat', 3, 5, 10, 'Görsel iletişim ve estetik üzerine odaklanır.', 'https://roadmap.sh/design'),
            ('Veri Bilimci', 'Teknoloji', 10, 3, 5, 'Verileri analiz ederek geleceği tahmin eder.', 'https://roadmap.sh/ai-data-scientist'),
            ('Dijital Pazarlama Uzmanı', 'İşletme', 6, 9, 7, 'Markaların dijital dünyadaki sesidir.', 'https://learndigital.withgoogle.com/digitalgarage'),
            ('Psikolog', 'Sosyal', 5, 10, 4, 'İnsan davranışlarını ve zihnini inceler.', 'https://www.apa.org/education-career'),
            ('Siber Güvenlik Uzmanı', 'Teknoloji', 9, 2, 5, 'Sistemleri dijital saldırılara karşı korur.', 'https://roadmap.sh/cyber-security'),
            ('İç Mimar', 'Tasarım', 6, 6, 9, 'Mekanları estetik ve fonksiyonel tasarlar.', 'https://www.archdaily.com'),
            ('Yapay Zeka Mühendisi', 'Teknoloji', 10, 4, 8, 'Kendi kendine öğrenebilen sistemler kurar.', 'https://roadmap.sh/ai'),
            ('Proje Yöneticisi', 'İşletme', 7, 10, 5, 'Ekipleri ve süreçleri hedefe ulaştırır.', 'https://www.pmi.org'),
            ('Oyun Geliştirici', 'Teknoloji', 8, 5, 10, 'Sanal dünyalar ve interaktif eğlence yaratır.', 'https://roadmap.sh/game-developer'),
            ('Avukat', 'Hukuk', 8, 9, 4, 'Hakları savunur ve hukuki sorunları çözer.', 'https://www.barobirlik.org.tr'),
            ('Genel Cerrah', 'Sağlık', 9, 7, 4, 'Ameliyatlarla hastalıkları tedavi eder.', 'https://www.facs.org'),
            ('Makine Mühendisi', 'Mühendislik', 10, 4, 6, 'Mekanik sistemler tasarlar ve üretir.', 'https://www.mmo.org.tr'),
            ('İnsan Kaynakları Uzmanı', 'İşletme', 4, 10, 4, 'Şirketlerin en değerli varlığı olan insanı yönetir.', 'https://www.shrm.org'),
            ('Müzisyen/Besteci', 'Sanat', 4, 4, 10, 'Seslerle duyguları ifade eder ve eserler yaratır.', 'https://www.berklee.edu'),
            ('Şef (Gastronomi)', 'Hizmet', 5, 5, 9, 'Lezzetli ve estetik yemekler tasarlar.', 'https://www.michelin.com'),
            ('Yatırım Uzmanı', 'Finans', 9, 6, 3, 'Parayı yönetir ve karlı yatırımlar planlar.', 'https://www.cfainstitute.org'),
            ('Öğretmen', 'Eğitim', 5, 10, 6, 'Bilgiyi aktarır ve gelecek nesilleri şekillendirir.', 'https://www.meb.gov.tr'),
            ('Biyolog', 'Bilim', 9, 3, 4, 'Canlıları ve yaşam süreçlerini inceler.', 'https://www.aibs.org'),
            ('Sosyal Medya Yöneticisi', 'Medya', 5, 9, 8, 'Markaların online topluluklarını yönetir.', 'https://blog.hubspot.com/marketing'),
            ('Moda Tasarımcısı', 'Tasarım', 3, 5, 10, 'Giyim trendlerini belirler ve kıyafet tasarlar.', 'https://www.vogue.com/fashion'),
            ('Pilot', 'Havacılık', 9, 4, 3, 'Uçakları güvenle uçurur ve seyahati sağlar.', 'https://www.faa.gov'),
            ('Psikiyatrist', 'Sağlık', 8, 9, 3, 'Ruhsal hastalıkları tıbbi yöntemlerle tedavi eder.', 'https://www.psychiatry.org'),
            ('Yazar/Senarist', 'Sanat', 4, 4, 10, 'Kelimelerle dünyalar ve hikayeler kurar.', 'https://writersguild.org'),
            ('İnşaat Mühendisi', 'Mühendislik', 9, 5, 5, 'Binalar, köprüler ve altyapılar inşa eder.', 'https://www.imo.org.tr'),
            ('Arkeolog', 'Bilim', 8, 3, 5, 'Geçmiş uygarlıkları kalıntılarla araştırır.', 'https://www.archaeological.org'),
            ('Diyetisyen', 'Sağlık', 7, 8, 4, 'Sağlıklı beslenme planları oluşturur.', 'https://www.eatright.org'),
            ('Etkinlik Organizatörü', 'İşletme', 4, 10, 7, 'Büyük organizasyonları ve davetleri planlar.', 'https://www.ises.com'),
            ('Çevirmen', 'Dil', 6, 5, 5, 'Kültürler ve diller arasında köprü kurar.', 'https://www.atanet.org'),
            ('Robotik Mühendisi', 'Teknoloji', 10, 3, 8, 'Robotlar ve otonom sistemler geliştirir.', 'https://www.ieee-ras.org')
        ]

        added_count = 0
        for meslek in meslekler:
            title = meslek[0]
            # Meslek var mı kontrol et
            self.cursor.execute("SELECT id FROM careers WHERE title = ?", (title,))
            if not self.cursor.fetchone():
                self.cursor.execute('''
                    INSERT INTO careers (title, field, score_analitik, score_sosyal, score_yaraticilik, description, roadmap_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', meslek)
                added_count += 1
        
        self.conn.commit()
        if added_count > 0:
            print(f" {added_count} yeni meslek veritabanına eklendi!")
        else:
            print("Veritabanı güncel, yeni eklenecek meslek yok.")

    def get_all_careers(self):
        self.cursor.execute("SELECT * FROM careers")
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def update_user_scores(self, user_id, username, scores):
        # scores: {'analitik': 5, 'sosyal': 3, ...}
        # Önce kullanıcı var mı kontrol et
        self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        
        # Puanları güncelle
        self.cursor.execute('''
            UPDATE users 
            SET u_analitik = ?, u_sosyal = ?, u_yaraticilik = ?
            WHERE user_id = ?
        ''', (scores.get('analitik', 0), scores.get('sosyal', 0), scores.get('yaraticilik', 0), user_id))
        self.conn.commit()

if __name__ == "__main__":
    db = CareerBotDB()
    db.add_sample_data()
    print("Veritabanı dosyası ve tablolar hazır!")