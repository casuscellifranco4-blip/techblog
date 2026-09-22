#!/usr/bin/env bash
# Script de build para Render. Se ejecuta automáticamente en cada despliegue.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_admin
python manage.py seed_data
