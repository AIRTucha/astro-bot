# Use an official Python runtime as a parent image
FROM python:3.10.5-slim-buster as base

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


FROM base as development

CMD ["python", "main.py"]

FROM base as production

# Copy the current directory contents into the container at /app
COPY . .

# Run the command to start your application
CMD ["python", "main.py"]