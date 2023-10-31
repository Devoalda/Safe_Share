#!/bin/bash

# Migrate the database (if needed)
python manage.py migrate --noinput

# Start your Django server in the background
python manage.py runserver 0.0.0.0:8000 &

# Start virus scanning service
python safeshare_vdb/server.py &

# Sleep briefly to allow the Django server to start (you can adjust the sleep duration as needed)
sleep 2

# Start the custom management command to run the trash collector
python manage.py start_trash_collector

# Optionally, you can monitor the logs in real-time if needed
tail -f django_server.log trash_collector.log
