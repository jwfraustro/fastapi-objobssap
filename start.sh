#!/bin/sh
set -e

alembic upgrade head

uvicorn fastapi_objobssap.main:app --host 0.0.0.0 --port $PORT