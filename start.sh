#!/bin/sh
set -e

uvicorn fastapi_objobssap.main:app --host "" --port ${PORT:-8000}