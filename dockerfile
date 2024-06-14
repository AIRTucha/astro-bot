# Use an official Python runtime as a parent image
FROM python:3.11.9-slim as base

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    build-essential

# Install Poetry
RUN pip install poetry

# Set the working directory in the container to /app
WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi


FROM base as dev

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]


FROM base as prod

COPY cert/ ../root/

# Copy the current directory contents into the container at /app
COPY . .

# Run the command to start your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]