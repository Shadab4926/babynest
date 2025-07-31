#!/usr/bin/env bash

# Step 1: Install all required libraries from requirements.txt
pip install -r requirements.txt

# Step 2: Django database migrate
python manage.py migrate

# Step 3: Collect static files (CSS, JS, etc)
python manage.py collectstatic --noinput
