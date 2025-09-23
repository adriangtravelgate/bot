import discord
import os
from dotenv import load_dotenv
from scheduler import start_scheduler

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    start_scheduler(bot)

bot.run(TOKEN)