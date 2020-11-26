#!/bin/sh

echo "Runnning Requirements.txt"
yes | pip install -r requirements.txt

echo "Runnning Database Migrations..."
yes | python manage.py migrate

echo "Runnning CollectStatic..."
yes | python manage.py collectstatic --no-input

echo "starting $@"
exec "$@"
