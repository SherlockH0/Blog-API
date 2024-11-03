#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python -m blogapi.manage'

echo "Running migrations..."
$RUN_MANAGE_PY migrate --no-input

echo "Running runserver on port 8000..."
$RUN_MANAGE_PY runserver 0.0.0.0:8000
