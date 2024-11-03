#!/bin/bash
set -e
sh -c 'scripts/wait-for-it.sh db:5432 -t 30'
exec "$@"

