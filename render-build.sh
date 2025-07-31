#!/usr/bin/env bash


echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Collecting static files..."
python manage.py collectstatic --noinput






#!/usr/bin/env bash
# render-build.sh



