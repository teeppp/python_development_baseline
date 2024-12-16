FROM python:3.12-slim AS base

# install UV
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

RUN apt-get update -y && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    graphviz graphviz-dev


FROM base AS backend
COPY ./backend /backend

WORKDIR /backend
RUN uv sync --frozen --no-cache

# uvicornでアプリケーションを起動
# CMD ["/backend/.venv/bin/fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8080"]
CMD ["uv", "run", "fastapi","run", "main.py", "--host", "0.0.0.0", "--port", "8080"]


FROM base AS frontend
COPY ./frontend /frontend

WORKDIR /frontend
RUN uv sync --frozen --no-cache

# Streamlitを起動
CMD ["uv","run","streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8080"]