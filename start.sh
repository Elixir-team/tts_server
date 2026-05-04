#!/bin/sh

set -eu

cd /app

exec python server.py \
  --host "${HOST:-0.0.0.0}" \
  --port "${PORT:-8000}"
