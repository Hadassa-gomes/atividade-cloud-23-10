#!/usr/bin/env bash
set -euo pipefail
export PORT=${PORT:-8000}
# App Service provides $PORT; default to 8000 locally
exec gunicorn -w 4 -k gthread -b 0.0.0.0:${PORT} app:app
