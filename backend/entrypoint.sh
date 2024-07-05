#!/bin/bash

echo "Waiting for the db"
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do 
    sleep 1
done
echo "DB is ready"

echo "Applying DB migration..."
python manage.py migrate

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:3000