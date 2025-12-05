#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Use direct connection for migrations (port 5432 instead of pooler)
# Replace pooler URL with direct connection
DIRECT_URL="${DATABASE_URL//6543/5432}"
DIRECT_URL="${DIRECT_URL//\?pgbouncer=true/}"
echo "Running migrations..."
DATABASE_URL="$DIRECT_URL" python manage.py migrate --noinput
