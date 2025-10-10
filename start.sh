#!/bin/sh
set -e

uvicorn fastapi_objobssap.main:app --host 0.0.0.0 --port $PORT