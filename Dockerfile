FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM base AS builder

COPY pyproject.toml uv.lock* ./

ARG ENVIRONMENT=production

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

RUN if [ "$ENVIRONMENT" = "production" ]; then \
        uv sync --no-dev; \
    else \
        uv sync; \
    fi

FROM python:3.13-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y libpq5 curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

COPY alembic.ini ./
COPY alembic ./alembic
COPY ./src ./src
COPY ./entrypoints ./entrypoints


EXPOSE 8000

ARG ENVIRONMENT=production
ENV ENVIRONMENT=${ENVIRONMENT}




RUN chown -R appuser:appuser /app || true
USER appuser

EXPOSE 8000


CMD ["sh", "entrypoints/web_entrypoint.sh"]