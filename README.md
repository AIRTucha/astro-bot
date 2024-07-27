Migrations:

poetry run alembic revision --autogenerate -m "Create a baseline migrations"
poetry run alembic upgrade head
poetry run alembic downgrade -1
poetry run alembic revision -m "Create trigger on students table"


export DATABASE_URL=postgresql+psycopg2://postgres:local_password@localhost:5432/astro-db