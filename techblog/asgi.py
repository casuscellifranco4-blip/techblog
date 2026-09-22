"""
Configuración ASGI para el proyecto techblog.

Expone la variable a nivel de módulo ``application``.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techblog.settings')

application = get_asgi_application()
