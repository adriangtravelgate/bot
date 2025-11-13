from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from utils import enviar_mensajes_y_crear_hilos, revisar_reacciones_y_mencionar

scheduler = AsyncIOScheduler()

def start_scheduler():
    # Iniciar scheduler si no esta ya iniciado
    if not scheduler.running:
        scheduler.start()

def programar_revision(bot):
    # Comprobación de si el job está iniciado en scheduler para evitar que haga un bucle, 
    # si ya existe el job lo elimina para crear uno nuevo
    if scheduler.get_job('revisar_reacciones'):
        scheduler.remove_job('revisar_reacciones')

    # Tiempo con el que se comprueban las reacciones de los hilos tras mandar el mensaje
    run_time = datetime.now() + timedelta(minutes=1)
    
    scheduler.add_job(
        revisar_reacciones_y_mencionar,
        'date',
        run_date=run_time,
        id='revisar_reacciones',
        args=[bot]
    )

def programar_envio_mensajes(bot):
    # Comprobación de si el job está iniciado en scheduler para evitar que haga un bucle, 
    # si ya existe el job lo elimina para crear uno nuevo
    if scheduler.get_job('enviar_mensajes'):
        scheduler.remove_job('enviar_mensajes')

    async def job_wrapper():
        # Envío de mensajes y creación de hilos
        resultado = await enviar_mensajes_y_crear_hilos(bot)
        # Si se ha enviado bien revisar las reacciones
        if resultado:
            programar_revision(bot)
            
    next_run_time = datetime.now() + timedelta(days=14)

    scheduler.add_job(
        job_wrapper,
        'interval',
        days=14,
        # Ejecutar el comando cada dos semanas, siempre y que no se apague el bot
        next_run_time=datetime.now(),
        id='enviar_mensajes'
    )