#!/usr/bin/env bash

touch render-build.sh
echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Collecting static files..."
python manage.py collectstatic --noinput
chmod +x render-build.sh







#!/usr/bin/env bash
# render-build.sh



