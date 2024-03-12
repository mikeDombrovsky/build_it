#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
#python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput \
    --username $SUPER_USERNAME \
    --email $SUPER_EMAIL \
    --password $SUPER_PASSWORD