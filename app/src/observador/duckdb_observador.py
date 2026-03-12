from datetime import datetime

import duckdb
import pandas as pd
from twitchAPI.object.api import Stream

from app.src.observador.observador import Observador


class DuckDBObservador(Observador[Stream]):
    def __init__(self):
        super().__init__()
        self.__con = duckdb.connect()
        self.__con.execute(
            "INSTALL httpfs"
        )
        self.__con.execute(
            "LOAD httpfs"
        )
        #           SET s3_endpoint='localhost:9000';         SET s3_endpoint='minio:9000';

        self.__con.execute(
            """
             SET s3_endpoint='minio:9000';
            SET s3_access_key_id='minio';
            SET s3_secret_access_key='minio123';
            SET s3_region='us-east-1';
            SET s3_url_style='path';
            SET s3_use_ssl=false;
            """
        )

    def atualizar_registro(self, dados: Stream) -> None:

        dt = dados.started_at.date()

        registro = [{
            "id": dados.id,
            "user_id": dados.user_id,
            "user_login": dados.user_login,
            "user_name": dados.user_name,
            "game_id": dados.game_id,
            "game_name": dados.game_name,
            "type": dados.type,
            "title": dados.title,
            "viewer_count": dados.viewer_count,
            "language": dados.language,
            "started_at": dados.started_at,
            "is_mature": dados.is_mature,
            "thumbnail_url": dados.thumbnail_url,
            "tags": dados.tags
        }]

        df = pd.DataFrame(registro)


        self.__con.register("stream_df", df)

        file_name = datetime.now().strftime("%H%M%S")

        path = f"s3://bronze/twitch/streams/dt={dt}/game={dados.game_id}/user_id={dados.user_id}/{file_name}.parquet"

        self.__con.execute(f"""
            COPY (SELECT * FROM stream_df)
            TO '{path}'
            (FORMAT PARQUET);
        """)
