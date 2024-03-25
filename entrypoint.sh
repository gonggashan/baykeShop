#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput --clear

# Initialize necessary data
echo "Initialize necessary data"
python manage.py initdata

# Start sqlite_web
echo "Starting sqlite_web for database panel"
sqlite_web ./db.sqlite3 -p 8001 -H 0.0.0.0 > sqlite_web.log 2>&1 &

# Start the main process
echo "Starting Django runserver"
python manage.py runserver 0.0.0.0:8000
