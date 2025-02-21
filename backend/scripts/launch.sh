#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

./scripts/wait-for-it.sh db:5432 -t 5

alembic upgrade head

exec "$@"
