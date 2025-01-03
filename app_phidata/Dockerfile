FROM python:3.12-slim AS base

RUN apt-get update -y && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    graphviz graphviz-dev

FROM base AS base_uv
# install UV
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

# Sample Project 
FROM base_uv AS base_backend
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=./backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=./backend/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

FROM base AS backend
COPY --from=base_backend --chown=app:app /app/.venv /app/.venv
COPY ./backend /app
WORKDIR /app
CMD ["/app/.venv/bin/fastapi","run", "api.py", "--host", "0.0.0.0", "--port", "8080"]

FROM base_uv AS base_frontend
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=./frontend/uv.lock,target=uv.lock \
    --mount=type=bind,source=./frontend/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

FROM base AS frontend
COPY --from=base_frontend --chown=app:app /app/.venv /app/.venv
COPY ./frontend /app
WORKDIR /app
CMD ["/app/.venv/bin/gunicorn","--bind", "0.0.0.0:8080", "main:me"]
