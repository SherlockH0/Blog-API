#!/usr/bin/env bash

set -e
poetry run python -m blogapi.manage rqworker default
