FROM python:3.13-slim

WORKDIR /src

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* README.md* ./

RUN poetry install --only main --no-root --no-interaction --no-ansi

COPY . .

CMD ["python", "db_ingestion.py"]