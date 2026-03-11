import asyncio
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from twitchAPI.object.api import Stream
from twitchAPI.twitch import Twitch

from app.src.assunto.assunto import Assunto
from app.src.observador.duckdb_observador import DuckDBObservador

load_dotenv()
CLIENTE_SECRET = os.getenv("CLIENTE_SECRET")
CLIENTE_ID = os.getenv("CLIENTE_ID")


async def main():
    twitch = Twitch(CLIENTE_ID, CLIENTE_SECRET)

    await twitch.authenticate_app([])

    assunto = Assunto[Stream]()
    duckdb_observador = DuckDBObservador()
    assunto.anexar_observador(duckdb_observador)

    # data atual em UTC
    today = datetime.now(timezone.utc).date()

    async for stream in twitch.get_streams(language=['pt']):
        started_at = stream.started_at

        if started_at.date() == today:
            print(
                stream
            )
            print(type(stream))
            assunto.notificar_observador(dados=stream)
            break


asyncio.run(main())
