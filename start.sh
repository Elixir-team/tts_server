#!/bin/sh

set -eu

cd /app

exec python server.py \
  --host "${HOST:-0.0.0.0}" \
  --port "${PORT:-8000}" \
  --slow-request-seconds "${SLOW_REQUEST_SECONDS:-1.0}" \
  --default-media-type "${DEFAULT_MEDIA_TYPE:-audio/mpeg}"
