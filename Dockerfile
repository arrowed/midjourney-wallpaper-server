FROM python:3.13-slim

WORKDIR /app

# directory with a .env file to pull config and secrets from
VOLUME /app/env

# static web files to serve
VOLUME /app/static_web

EXPOSE 8080

# root dir of wallpapers
VOLUME /app/wallpapers

COPY requirements.txt /app/requirements.txt

RUN python -m venv /app/venv && \
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY *.py /app
COPY decorators /app/decorators

ENTRYPOINT [ "python", "app.py" ]