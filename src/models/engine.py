from sqlalchemy import create_engine

import os

engine = create_engine(
    os.getenv("DATABASE_URL"),
    echo=False,
    connect_args={"connect_timeout": 10},
)
