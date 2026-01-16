import discord
from discord.ext import commands
import config
from database.database import CareerBotDB
from modules import calculator, reporter
from modules.ui_components import CareerQuizView

# 1. Botu Tanımla
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 2. Veritabanını Bağla
db = CareerBotDB(config.DB_PATH)

@bot.event
async def on_ready():
    # Meslekleri kontrol et ve ekle
    db.add_sample_data()
    print(f"{bot.user} olarak giriş yapıldı!")
    print("--------------------------------")

@bot.command()
async def merhaba(ctx):
    await ctx.send(f"Merhaba {ctx.author.name}! Meslek danışmanı botuna hoş geldin. Başlamak için `!kariyer` yazabilirsin.")

@bot.command()
async def kariyer(ctx):
    view = CareerQuizView(db, calculator, reporter, ctx.author.id, ctx.author.name)
    await ctx.send(f"Merhaba **{ctx.author.name}**! Seni tanımak için birkaç soru soracağım.\n\n**Soru 1:** {view.questions[0]['text']}", view=view)

# 3. Botu Çalıştır
if __name__ == "__main__":
    bot.run(config.TOKEN)