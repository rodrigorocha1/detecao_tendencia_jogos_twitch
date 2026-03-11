import json
import os
from datetime import datetime
from typing import Dict, List, Union

import duckdb
import pandas as pd



pd.set_option('display.max_columns', None)
pd.set_option('display.width', 3000)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', '{:.2f}'.format)


class BancoS3(IServicoS3):

    def __init__(self):
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


            SET s3_endpoint='localhost:9000'; 
            SET s3_access_key_id='minio';
            SET s3_secret_access_key='minio123';
            SET s3_region='us-east-1';
            SET s3_url_style='path';
            SET s3_use_ssl=false;
            """
        )