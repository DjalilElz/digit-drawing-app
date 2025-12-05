#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Remove pgbouncer parameter for migrations (not supported)
export MIGRATION_DB_URL="${DATABASE_URL/\?pgbouncer=true/}"
DATABASE_URL="$MIGRATION_DB_URL" python manage.py migrate
