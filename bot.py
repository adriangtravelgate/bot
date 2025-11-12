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
bot = commands.Bot(command_prefix="/", intents=intents)

# Slash command: /condecorar 
# activar entorno antes (venv\Scripts\activate) y luego lanzar el bot (python bot.py)
@bot.tree.command(name="condecorar", description="Inicia las condecoraciones.")
async def condecorar(interaction: discord.Interaction):
    try:
        start_scheduler()
        programar_envio_mensajes(bot)
        # Mensaje al ejecutar el comando, para que solo se vea unos segundos el usuario que lo ha ejecutado
        await interaction.response.send_message("Iniciando condecoraciones.", ephemeral=True)
    except Exception as e:
        # Mensaje de error en caso de fallo, no debería saltar y si sale saldrá el 
        # predeterminado de discord porque el bot no esté funcional, se añade en caso de alguna otra excepción
        await interaction.response.send_message(f"Error al iniciar las condecoraciones: {e}", ephemeral=True)

# Ejecutar el bot
bot.run(TOKEN)