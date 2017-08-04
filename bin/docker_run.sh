#!/bin/bash

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_NAME", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="$POSTGRES_HOST")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."

python manage.py migrate                  # Apply database migrations
python manage.py createsu

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn PyInvoice.wsgi:application \
    --bind 0.0.0.0:301 \
    --workers 3
    "$@"
