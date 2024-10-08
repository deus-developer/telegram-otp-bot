FROM python:3.11-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
RUN uv pip install tgcrypto --system
RUN uv pip install https://github.com/KurimuzonAkuma/pyrogram/archive/v2.1.29.zip --system

COPY main.py /app

ENTRYPOINT ["python", "main.py"]