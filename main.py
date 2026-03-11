import asyncio
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from twitchAPI.twitch import Twitch

load_dotenv()
CLIENTE_SECRET = os.getenv("CLIENTE_SECRET")
CLIENTE_ID = os.getenv("CLIENTE_ID")


async def main():
    twitch = Twitch(CLIENTE_ID, CLIENTE_SECRET)

    await twitch.authenticate_app([])

    # data atual em UTC
    today = datetime.now(timezone.utc).date()

    async for stream in twitch.get_streams(language=['pt']):
        started_at = stream.started_at

        # verificar se começou hoje
        if started_at.date() == today:
            print(
               stream
            )


asyncio.run(main())