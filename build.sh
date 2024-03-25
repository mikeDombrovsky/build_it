#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

python manage.py createsuperuser --noinput --username admin --email admin@gmail.com || true