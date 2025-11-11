from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from utils import enviar_mensajes_y_crear_hilos, revisar_reacciones_y_mencionar

scheduler = AsyncIOScheduler()

def start_scheduler():
    # Iniciar scheduler si no esta ya iniciado
    if not scheduler.running:
        scheduler.start()
        print("✅ Scheduler iniciado")

def programar_revision(bot):
    # Comprobación de si scheduler está iniciado para evitar que haga un bucle, hasta siguientes condecoraciones no se vuelve a añadir el job
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
    # Para comprobar en consola cuando se revisa/envia el mensaje con ganadores, se puede quitar al subir el bot mas tarde ya que realmente no hace nada
    print(f"⏳ Job de revisión programado para {run_time.strftime('%Y-%m-%d %H:%M:%S')}")

def programar_envio_mensajes(bot):
    # Misma comprobación que con la función de antes
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
        next_run_time=datetime.now(),  # Para pruebas inmediatas, borrar al subir el bot
        id='enviar_mensajes'
    )
    # Mismo que el otro, borrar al subir el bot
    print(f"📅 Job de envío de mensajes programado para las {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")