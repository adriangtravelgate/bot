import os
import discord
import json
from dotenv import load_dotenv

# Carga del canal de discord, rol y usuario fantasma (cambiar en el .env si se prueba en otro canal)
load_dotenv()
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
GUILD_ID = int(os.getenv('GUILD_ID'))
ROLE_ID = int(os.getenv('ROLE_ID'))
FANTASMA_ID = int(os.getenv('FANTASMA_ID'))

# Archivo donde se guardaran los condecorados
DATA_FILE = 'hilos_info.json'

def cargar_datos():
    # Lectura del archivo donde se almacenan los condecorados
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_datos(data):
    # Escritura de condecorados al revisar reacciones
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def enviar_mensajes_y_crear_hilos(bot):
    # Canal en el que el bot mandará los mensajes (cambiar channel_id en el .env)
    canal = bot.get_channel(CHANNEL_ID)

    # ID del Rol al que mencionará el bot para las condecoraciones (Service Integration)
    roleId = ROLE_ID

    # Mensajes que enviará el bot al ejecutarse
    mensajes = [
        {
            "contenido": f"A los buenos días, a por otras putísimas condecoracionees <@&{roleId}> 😎",
            "hilo": None
        },
        {
            "contenido": "Team's Sunshine ☀️ \n Condecoración a persona que ha mantenido en alto el humor del equipo",
            "hilo": "Team's Sunshine ☀️"
        },
        {
            "contenido": "Helping Hand 🤝 \n Condecoración a persona que lo ha dado todo por ayudar a los compañeros esta semanas.",
            "hilo": "Helping Hand 🤝"
        },
        {
            "contenido": "Defender 🛡️\n Condecoración a persona que ha resistido la furia de los proveedores",
            "hilo": "Defender 🛡️"
        },
        {
            "contenido": "Good Programer 🧭 \n Condecoración a persona que ha aplicado mejoras interesantes a nivel técnico",
            "hilo": "Good Programer 🧭"
        },
        {
            "contenido": "Fantasma del equipo 👻 \n Condecoración a persona que no aparece a ningún evento ni aunque le pagasen",
            "hilo": "Fantasma del equipo 👻"
        }
    ]

    # Leemos el archivo generado antes
    data = cargar_datos()

    # Por cada mensaje guardamos el nombre del hilo y el mensaje en el que se creará el hilo
    for item in mensajes:
        condecoracion = item["contenido"]
        hilo = item["hilo"]

        # Permisos del bot para mencionar
        msg = await canal.send(
            content=condecoracion,
            allowed_mentions=discord.AllowedMentions(roles=True, users=True)
        )

        # Si el mensaje tiene hilo (el que menciona a Service Integration no tiene) crea un hilo con el nombre de este 
        if hilo:
            hilo = await canal.create_thread(
                name=hilo,
                message=msg
            )

            # Crea array con los ID de los usuarios mencionados en los hilos
            usuarios_mencionados = [user.id for user in msg.mentions]

            data[str(hilo.id)] = {
                "thread_id": hilo.id,
                "message_id": msg.id,
                "user_ids": usuarios_mencionados
            }
    # Guarda los datos almacenados
    guardar_datos(data)
    
    # Devuelve true para no hacer un bucle infinito
    return True


async def revisar_reacciones_y_mencionar(bot):
    # Volvemos a cargar los datos del archivo generado antes
    data = cargar_datos()
    # Si esta vacío interrumpimos la operación
    if not data:
        return False

    resumen = {}  # Diccionario para el resumen final

    # Iteramos en cada hilo que se haya guardado en el archivo anterior
    for hilo_id_str, info in data.items():
        
        hilo_id = int(hilo_id_str)
        hilo = bot.get_channel(hilo_id)

        # Si no existe el hilo continúa con el siguiente
        if not isinstance(hilo, discord.Thread):
            continue

        try:
            # Variable original_canal coge el canal en el que se crea el hilo
            original_canal = hilo.parent
            # Control de errores por si no se encuentra el canal
        except discord.NotFound:
            continue
        except Exception as e:
            continue

        # Obtener todos los mensajes del hilo
        mensajes = [msg async for msg in hilo.history(limit=None)]

        # Buscar el mensaje con más reacciones, contando la reaccion 👍 como votos
        Votos = '👍'

        mensaje_mas_reaccionado = max(
            mensajes,
            key=lambda m: next((r.count for r in m.reactions if str(r.emoji) == Votos), 0),
            default=None
        )

        # Obtener menciones del mensaje más reaccionado
        menciones = mensaje_mas_reaccionado.mentions
        fantasmaId = FANTASMA_ID
        
        if hilo.name == "Fantasma del equipo 👻":
            # Mencionar siempre al mismo usuario para la condecoración de fantasma, buscando su ID de usuario
            resumen[hilo.name] = [u.mention for u in bot.get_all_members() if u.id == fantasmaId]
            continue
        
        if not menciones:
            # Si no hay ninguna mención establecer que no hay ganadores
            resumen[hilo.name] = ["Ningún ganador"]
            continue

        # Guardar ganadores en resumen
        resumen[hilo.name] = [u.mention for u in menciones]

    # Creamos el mensaje para los condecorados

    resumen_texto = "Los medallistas: \n\n"
    for categoria, ganadores in resumen.items():
        # Aquí pasamos los ganadores a string ya que para establecer el fantasma del equipo por id lo hacemos con un int y peta
           resumen_texto += f"- **{categoria}**: {', '.join(str(g) for g in ganadores)}\n"
        # Enviamos el mensaje de condecorados
    await original_canal.send(resumen_texto)

    # Limpiar archivo para el conteo de las siguientes condecoraciones
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write("{}")
        
    return True