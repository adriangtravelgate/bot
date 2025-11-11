import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from scheduler import start_scheduler, programar_envio_mensajes

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

# Crear el bot con soporte de comandos
bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ Evento al iniciar
@bot.event
# Comando para ejecutar el bot, activar entorno antes (venv\Scripts\activate) y luego lanzar el bot (python bot.py)
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comandos sincronizados.")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

# Slash command: /condecorar
@bot.tree.command(name="condecorar", description="Inicia las condecoraciones.")
async def condecorar(interaction: discord.Interaction):
    try:
        start_scheduler()
        programar_envio_mensajes(bot)
        await interaction.response.send_message("Iniciando condecoraciones.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Error al iniciar las condecoraciones: {e}", ephemeral=True)
        print(f"Error al iniciar condecoraciones: {e}")

# Ejecutar el bot
bot.run(TOKEN)