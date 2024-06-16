from sqlalchemy import create_engine

import os

database_url = os.getenv("DATABASE_URL")

if database_url is None:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(
    database_url,
    echo=False,
    connect_args={"connect_timeout": 10},
)
