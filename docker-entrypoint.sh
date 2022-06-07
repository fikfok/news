#!/bin/bash
set -e

if [ "$1" = "uvicorn" ]; then
    echo "Waiting for postgres..."
    while ! nc -z $POSTGRESQL_HOST $POSTGRESQL_PORT; do
        sleep 5
    done
    echo "PostgreSQL started"
    echo "Apply database migrations"
    cd adfox_int
    alembic upgrade heads
fi

if [ "$1" = "celery" ]; then
    echo "Waiting for postgres..."
    while ! nc -z $POSTGRESQL_HOST $POSTGRESQL_PORT; do
        sleep 5
    done
    echo "PostgreSQL started"
    echo "Apply database migrations"
    alembic upgrade heads
fi

exec "$@"
