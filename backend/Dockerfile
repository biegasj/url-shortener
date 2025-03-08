FROM python:3.12.9-bullseye AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

RUN pip install poetry~=2.0.1

COPY pyproject.toml poetry.lock alembic.ini ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.12.9-slim-bullseye AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . .

RUN chmod +x scripts/*.sh

EXPOSE 8000

FROM runtime AS dev
ENTRYPOINT ["bash", "scripts/launch.sh"]
CMD ["uvicorn", "app.main:app", "--port=8000", "--host=0.0.0.0", "--proxy-headers", "--reload"]

FROM runtime AS prod
ENTRYPOINT ["bash", "scripts/launch.sh"]
CMD ["uvicorn", "app.main:app", "--port=8000", "--host=0.0.0.0", "--proxy-headers"]
