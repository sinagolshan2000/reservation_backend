#!/bin/sh

set -e

# Wait for Postgres to be ready
echo "Waiting for database..."
until nc -z db 5432; do
  sleep 1
done
echo "Database is up!"

# Run migrations
python manage.py migrate --noinput

# Start the server
exec "$@"

