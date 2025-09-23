import discord
import os
from dotenv import load_dotenv
from scheduler import start_scheduler, programar_envio_mensajes

# Carga de entorno y token del bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Permisos del bot para manejar el canal de discord 
intents = discord.Intents.default()

intents.message_content = True   # Enviar mensajes y crear hilos
intents.reactions = True         # Conteo de reacciones
intents.members = True           # Mencionar miembros condecorados


bot = discord.Client(intents=intents)

@bot.event
# Comando para ejecutar el bot, activar entorno antes (venv\Scripts\activate) y luego lanzar el bot (python bot.py)
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    start_scheduler()
    programar_envio_mensajes(bot)


bot.run(TOKEN)