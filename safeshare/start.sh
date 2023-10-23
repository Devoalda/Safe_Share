#!/bin/bash

# Wait until Database is ready
while ! nc -z db 3306; do sleep 1; done

python manage.py migrate --noinput

# Seed the database with initial data
#python manage.py loaddata study_together_app/fixtures/*

python manage.py runserver 0.0.0.0:8000