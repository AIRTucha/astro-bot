Migrations:

poetry run alembic revision --autogenerate -m "Create a baseline migrations"
poetry run alembic upgrade head
poetry run alembic downgrade -1
poetry run alembic revision -m "Create trigger on students table"

curl --create-dirs -o $HOME/.postgresql/root.crt 'https://cockroachlabs.cloud/clusters/776aed44-bf61-4eb0-8b8d-de9f3affb84d/cert'