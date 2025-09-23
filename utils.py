
import os
import discord
from dotenv import load_dotenv

load_dotenv()
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

async def enviar_mensajes_y_crear_hilos(bot):
    print("🚀 Enviando mensajes programados...")

    canal = bot.get_channel(CHANNEL_ID)
    
    if canal is None:
        print("❌ Canal no encontrado.")
        return

    
    roleId = 1419979252945649674

    mensajes = [
        {
            "contenido": f"A los buenos días, a por otras putísimas condecoracionees <@&{roleId}> 😎",
            "hilo": None
        },
        {
            "contenido": "Team's Sunshine ☀️ /n Condecoración a persona que ha mantenido en alto el humor del equipo",
            "hilo": "Team's Sunshine ☀️"
        },
        {
            "contenido": "Helping Hand 🤝 /n Condecoración a persona que lo ha dado todo por ayudar a los compañeros esta semanas.",
            "hilo": "Helping Hand 🤝"
        },
        {
            "contenido": "Defender 🛡️/n Condecoración a persona que ha resistido la furia de los proveedores",
            "hilo": "Defender 🛡️"
        },
        {
            "contenido": "Good Programer 🧭 /n Condecoración a persona que ha aplicado mejoras interesantes a nivel técnico",
            "hilo": "Good Programer 🧭"
        },
        {
            "contenido": "Fantasma del equipo 👻 /n Condecoración a persona que no aparece a ningún evento ni aunque le pagasen",
            "hilo": "Fantasma del equipo 👻"
        }
    ]

    for item in mensajes:
        condecoracion = item["contenido"]
        hilo = item["hilo"]

        msg = await canal.send(
            content=condecoracion,
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

        if hilo:
            await canal.create_thread(
                name=hilo,
                message=msg
            )