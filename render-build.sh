#!/usr/bin/env bash

touch render-build.sh
echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Collecting static files..."
python manage.py collectstatic --noinput






#!/usr/bin/env bash
# render-build.sh



