"""
Configuración de Django para el proyecto TechBlog.

Proyecto final del curso de Python (Coderhouse) — Franco Casuscelli.
"""
from pathlib import Path

import dj_database_url
from decouple import Csv, config

# Construye rutas dentro del proyecto de esta forma: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------
# Seguridad
# ----------------------------------------------------------------------
# En producción, SECRET_KEY, DEBUG y ALLOWED_HOSTS se configuran mediante
# variables de entorno (ver .env.example). Nunca subas tu SECRET_KEY real
# al repositorio.
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-clave-de-desarrollo-cambiar-en-produccion',
)

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

# ----------------------------------------------------------------------
# Aplicaciones instaladas
# ----------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps propias del proyecto
    'blog',
    'accounts',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise sirve los archivos estáticos en producción sin necesidad
    # de un servidor web adicional (Nginx, etc.). Debe ir justo después de
    # SecurityMiddleware.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'techblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'techblog.wsgi.application'

# ----------------------------------------------------------------------
# Base de datos
# ----------------------------------------------------------------------
# En local, sin configurar nada, se usa SQLite. En Render (o cualquier otro
# servicio) se define la variable de entorno DATABASE_URL apuntando a la
# base de datos PostgreSQL provista por el servicio de despliegue.
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ----------------------------------------------------------------------
# Validación de contraseñas
# ----------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------------------------------------------------
# Internacionalización
# ----------------------------------------------------------------------
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------------------
# Archivos estáticos y media
# ----------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        # Sirve archivos estáticos comprimidos y con hash en el nombre
        # (cache-busting) sin depender de un servicio externo.
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ----------------------------------------------------------------------
# Autenticación
# ----------------------------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'pages:home'
LOGOUT_REDIRECT_URL = 'pages:home'

# ----------------------------------------------------------------------
# Seguridad adicional en producción (cuando DEBUG=False)
# ----------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
