#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python -m blogapi.manage'

echo "Running migrations..."
$RUN_MANAGE_PY migrate --no-input

$RUN_MANAGE_PY runserver
