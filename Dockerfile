FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    fonts-roboto \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser \
    && chown -R appuser /app

USER appuser

WORKDIR /app/src

CMD ["python", "main.py"]
