import discord
from discord.ui import View, Button

class CareerQuizView(View):
    def __init__(self, db, calculator, reporter, user_id, username):
        super().__init__(timeout=None)
        self.db = db
        self.calculator = calculator
        self.reporter = reporter
        self.user_id = user_id
        self.username = username
        
        self.scores = {'analitik': 0, 'sosyal': 0, 'yaraticilik': 0}
        self.current_step = 0
        
        # 30 Detaylı Soru (Her kategori için 10 adet)
        self.questions = [
            # Analitik Sorular (Mevcut)
            {"text": "Karmaşık problemleri küçük, yönetilebilir parçalara ayırarak çözmekten hoşlanır mısın?", "category": "analitik"},
            {"text": "Veriler, istatistikler ve grafikler üzerinden analiz yapıp sonuç çıkarmak ilgini çeker mi?", "category": "analitik"},
            {"text": "Bir makinenin veya yazılımın arka planında nasıl çalıştığını merak edip araştırır mısın?", "category": "analitik"},
            {"text": "Satranç, sudoku veya mantık bulmacalarıyla zihnini zorlamaktan keyif alır mısın?", "category": "analitik"},
            {"text": "Teknolojik gelişmeleri yakından takip edip yeni çıkan araçları hemen denemek ister misin?", "category": "analitik"},
            # Analitik Sorular (Yeni)
            {"text": "Detaylı planlar ve çizelgeler oluşturup bunlara sadık kalmak senin için önemli mi?", "category": "analitik"},
            {"text": "Bir sistemin hatasını bulup onu daha verimli hale getirmek için uğraşır mısın?", "category": "analitik"},
            {"text": "Karar verirken duygularından çok somut verilere ve gerçeklere mi güvenirsin?", "category": "analitik"},
            {"text": "Sebep-sonuç ilişkilerini incelemekten ve 'neden' sorusuna cevap aramaktan hoşlanır mısın?", "category": "analitik"},
            {"text": "Finansal tablolar veya kod satırları gibi yapılandırılmış verilerle çalışmak ilgini çeker mi?", "category": "analitik"},
            
            # Sosyal Sorular (Mevcut)
            {"text": "İnsanlara bildiğin bir şeyi öğretmek veya onlara rehberlik etmek seni mutlu eder mi?", "category": "sosyal"},
            {"text": "Grup çalışmalarında liderlik yapmayı veya iletişimi organize etmeyi sever misin?", "category": "sosyal"},
            {"text": "Tanımadığın insanlarla dolu bir ortamda kolayca iletişim kurup kaynaşabilir misin?", "category": "sosyal"},
            {"text": "Bir tartışmada veya anlaşmazlıkta insanları ikna etme yeteneğine güvenir misin?", "category": "sosyal"},
            {"text": "Topluluk önünde konuşma yapmak veya bir fikri sunmak senin için heyecan verici midir?", "category": "sosyal"},
            # Sosyal Sorular (Yeni)
            {"text": "İnsanların duygusal ihtiyaçlarını fark edip onlara destek olmak senin için doğal bir refleks mi?", "category": "sosyal"},
            {"text": "Başkalarının potansiyelini ortaya çıkarmasına yardımcı olmak seni motive eder mi?", "category": "sosyal"},
            {"text": "Bir ekip içinde uyumu sağlamak ve çatışmaları çözmekte başarılı olduğunu düşünür müsün?", "category": "sosyal"},
            {"text": "Farklı kültürlerden ve geçmişlerden gelen insanlarla tanışmak seni heyecanlandırır mı?", "category": "sosyal"},
            {"text": "Hizmet odaklı bir iş yaparak insanlara doğrudan fayda sağlamak ister misin?", "category": "sosyal"},
            
            # Yaratıcılık Soruları (Mevcut)
            {"text": "Zihninde canlandırdığın soyut bir fikri (resim, hikaye, proje) somutlaştırmayı sever misin?", "category": "yaraticilik"},
            {"text": "Olaylara herkesin baktığı açıdan değil, tamamen farklı bir perspektiften bakmayı dener misin?", "category": "yaraticilik"},
            {"text": "Bir ürünün veya ortamın estetik görünümü, renk uyumu ve tasarımı senin için önemli midir?", "category": "yaraticilik"},
            {"text": "Hazır şablonları kullanmak yerine kendi özgün tarzını oluşturmayı tercih eder misin?", "category": "yaraticilik"},
            {"text": "Müzik, resim, yazı gibi sanatsal aktivitelerle uğraşırken zamanın nasıl geçtiğini unutur musun?", "category": "yaraticilik"},
            # Yaratıcılık Soruları (Yeni)
            {"text": "Sıradan bir nesneyi alıp ona bambaşka bir işlev kazandırmayı hayal eder misin?", "category": "yaraticilik"},
            {"text": "Moda, dekorasyon veya mimari gibi görsel alanlardaki trendleri takip eder misin?", "category": "yaraticilik"},
            {"text": "Kurallara sıkı sıkıya bağlı kalmak yerine esnek ve doğaçlama çalışmayı mı tercih edersin?", "category": "yaraticilik"},
            {"text": "Hikaye anlatıcılığı veya senaryo yazımı gibi kurgusal dünyalar yaratmak ilgini çeker mi?", "category": "yaraticilik"},
            {"text": "Bir problemi çözerken daha önce hiç denenmemiş yolları denemekten korkmaz mısın?", "category": "yaraticilik"}
        ]
        
        self.create_buttons()

    def create_buttons(self):
        self.clear_items()
        
        if self.current_step < len(self.questions):
            q = self.questions[self.current_step]
            
            # İlerleme durumunu göster (Örn: Soru 1/15)
            progress = f"({self.current_step + 1}/{len(self.questions)})"
            
            btn_yes = Button(label="Evet", style=discord.ButtonStyle.green, custom_id="yes")
            btn_maybe = Button(label="🟡 Kısmen", style=discord.ButtonStyle.primary, custom_id="maybe")
            btn_no = Button(label="Hayır", style=discord.ButtonStyle.danger, custom_id="no")
            
            # Bu butonların ait olduğu adım (step)
            step_at_creation = self.current_step
            
            async def callback(interaction, score):
                # Eğer kullanıcı çok hızlı tıklarsa veya çift tıklarsa, 
                # ve biz zaten bir sonraki adıma geçtiysek, bu tıklamayı yoksay.
                if self.current_step != step_at_creation:
                    # Zaten işlem yapıldı, sadece defer edip çıkalım ki "interaction failed" demesin
                    await interaction.response.defer()
                    return

                category = q["category"]
                self.scores[category] += score
                self.current_step += 1
                await self.update_view(interaction)

            # Puanlama: Evet=3, Kısmen=1, Hayır=0
            btn_yes.callback = lambda i: callback(i, 3)
            btn_maybe.callback = lambda i: callback(i, 1)
            btn_no.callback = lambda i: callback(i, 0)
            
            self.add_item(btn_yes)
            self.add_item(btn_maybe)
            self.add_item(btn_no)
        else:
            pass

    async def update_view(self, interaction):
        if self.current_step < len(self.questions):
            self.create_buttons()
            progress = f"**Soru {self.current_step + 1}/{len(self.questions)}:**"
            await interaction.response.edit_message(content=f"{progress} {self.questions[self.current_step]['text']}", view=self)
        else:
            await interaction.response.defer()
            await self.finish_quiz(interaction)

    async def finish_quiz(self, interaction):
        # 0. Normalizasyon (0-30 arası ham puanı 0-10 arasına çek)
        # Maksimum puan = 10 soru * 3 puan = 30
        normalized_scores = {}
        for cat, score in self.scores.items():
            # (Ham Puan / 30) * 10 -> int
            norm_score = round((score / 30) * 10)
            normalized_scores[cat] = norm_score

        # 1. DB Güncelle (Normalize edilmiş puanlarla)
        self.db.update_user_scores(self.user_id, self.username, normalized_scores)
        
        # 2. En iyi 3 mesleği bul (yüzdelerle birlikte)
        careers = self.db.get_all_careers()
        from modules.calculator import calculate_top_careers
        top_matches = calculate_top_careers(normalized_scores, careers, top_n=3)
        
        # En iyi eşleşme (rapor ve kart için)
        best_match = top_matches[0]['career'] if top_matches else None
        best_percentage = top_matches[0]['match_percentage'] if top_matches else 0
        
        # 3. Rapor oluştur
        report_path = self.reporter.generate_report(self.username, normalized_scores, best_match)
        
        # 4. Görsel Kart Oluştur
        from modules.visualizer import CareerVisualizer
        viz = CareerVisualizer()
        card_path = viz.create_career_card(self.username, best_match, normalized_scores)
        
        # 5. Sonuçları gönder
        embed = discord.Embed(title=f"🎉 Tebrikler {self.username}!", color=0x3498db)
        embed.description = "Analiz tamamlandı! İşte sana en uygun 3 meslek:"
        
        # Top 3 meslekleri göster
        medals = ["🥇", "🥈", "🥉"]
        top_careers_text = ""
        for i, match in enumerate(top_matches):
            career = match['career']
            percentage = match['match_percentage']
            medal = medals[i] if i < len(medals) else "•"
            top_careers_text += f"{medal} **{career['title']}** - %{percentage} uyum\n"
        
        embed.add_field(name=" Kariyer Eşleşmelerin", value=top_careers_text, inline=False)
        
        # En iyi mesleğin detayı
        embed.add_field(name=f" 1. Tercih: {best_match['title']}", value=best_match['description'], inline=False)
        
        # Puanları da gösterelim
        scores_text = (
            f"**Analitik:** {normalized_scores['analitik']}/10\n"
            f"**Sosyal:** {normalized_scores['sosyal']}/10\n"
            f"**Yaratıcılık:** {normalized_scores['yaraticilik']}/10"
        )
        embed.add_field(name=" Kişilik Analizin", value=scores_text, inline=False)
        
        embed.set_image(url=f"attachment://card_{self.username}.png")
        embed.set_footer(text="Detaylı rapor ve görsel analiz ekte! ")
        
        file_report = discord.File(report_path, filename="KariyerRaporu.html")
        file_card = discord.File(card_path, filename=f"card_{self.username}.png")
        
        await interaction.followup.send(embed=embed, files=[file_report, file_card])
        self.stop()

