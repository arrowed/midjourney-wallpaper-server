#!/bin/sh

if [ ! -f "/app/.env" ]; then
    ln -s /app/env/.env /app/.env
fi

cd /app
source venv/bin/activate
python app.py