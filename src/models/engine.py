from sqlalchemy import create_engine
import psycopg2

engine = create_engine(
    "postgresql+psycopg2://postgres:local_password@db/astro-db",
    echo=False,
    connect_args={"connect_timeout": 10},
)
