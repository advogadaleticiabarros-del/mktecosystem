FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml alembic.ini ./
COPY app ./app
COPY alembic ./alembic

# libatomic1: o node que vem com o playwright novo precisa dela (build falhou com exit 127 em 10/11/2026).
RUN apt-get update && apt-get install -y --no-install-recommends libatomic1 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -e . \
    && playwright install --with-deps chromium

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
