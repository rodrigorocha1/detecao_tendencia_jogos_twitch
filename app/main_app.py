import asyncio
import os
import signal
import sys
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv
from twitchAPI.object.api import Stream
from twitchAPI.twitch import Twitch

from app.src.assunto.assunto import Assunto
from app.src.observador.duckdb_observador import DuckDBObservador
from app.src.utlis.utlis_log import logger

load_dotenv()

CLIENTE_SECRET = os.getenv("CLIENTE_SECRET")
CLIENTE_ID = os.getenv("CLIENTE_ID")

scheduler = AsyncIOScheduler()


async def coletar_streams():
    twitch = Twitch(CLIENTE_ID, CLIENTE_SECRET)
    await twitch.authenticate_app([])
    assunto = Assunto[Stream]()
    duckdb_observador = DuckDBObservador()
    assunto.anexar_observador(duckdb_observador)
    today = datetime.now(timezone.utc).date()
    logger.info('Coletando dados streams...')
    async for stream in twitch.get_streams(language=["pt"]):
        started_at = stream.started_at
        if started_at.date() == today:
            assunto.notificar_observador(dados=stream)
    await twitch.close()
    logger.info('Fim coleta dados streams...')


def desativar_rotina(signum, frame):
    logger.info("Encerrando scheduler...")
    scheduler.shutdown()
    sys.exit(0)


async def main():
    scheduler.add_job(
        coletar_streams,
        trigger=IntervalTrigger(minutes=15),
        id="job_15_min",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    logger.info("Scheduler iniciado...")

    # mantém o loop vivo
    while True:
        logger.info("Dentro do While True iniciado...")
        await asyncio.Event().wait()
        logger.info("FIM do While True iniciado...")



if __name__ == "__main__":
    signal.signal(signal.SIGTERM, desativar_rotina)
    signal.signal(signal.SIGINT, desativar_rotina)
    asyncio.run(coletar_streams())
    asyncio.run(main())
