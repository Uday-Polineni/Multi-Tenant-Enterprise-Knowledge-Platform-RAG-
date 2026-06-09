#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until python -c "
import os, sys
import psycopg2
psycopg2.connect(os.environ['DATABASE_URL'])
" 2>/dev/null; do
  sleep 2
done

echo "Running database migrations..."
alembic upgrade head

echo "Starting: $*"
exec "$@"
