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
CMD ["/app/.venv/bin/fastapi","run", "main.py", "--host", "0.0.0.0", "--port", "8080"]

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
CMD ["/app/.venv/bin/streamlit","run", "streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8080"]

# FROM base AS frontend
# COPY ./frontend /frontend

# WORKDIR /frontend
# RUN uv sync --frozen --no-cache

# # Streamlitを起動
# CMD ["uv","run","streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8080"]