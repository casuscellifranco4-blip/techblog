"""
Configuración WSGI para el proyecto techblog.

Expone la variable a nivel de módulo ``application``. Es el punto de
entrada que usa Gunicorn en producción (Render).
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techblog.settings')

application = get_wsgi_application()
