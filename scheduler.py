
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from utils import enviar_mensajes_y_crear_hilos

def start_scheduler(bot):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        enviar_mensajes_y_crear_hilos,
        'interval',
        days=14,
        next_run_time=datetime.now(),  # Ejecutar la primera vez al iniciar
        args=[bot]
    )

    scheduler.start()
