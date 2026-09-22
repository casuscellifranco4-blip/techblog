import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Crea un superusuario a partir de variables de entorno, si todavia no existe.

    Pensado para plataformas de despliegue (como Render) donde no hay una
    terminal interactiva disponible para correr `createsuperuser` a mano.

    Variables de entorno usadas:
        ADMIN_USERNAME
        ADMIN_EMAIL   (opcional)
        ADMIN_PASSWORD

    Si falta el usuario o la contraseña, el comando no hace nada (no
    rompe el build). Es seguro correrlo en cada despliegue: si el
    superusuario ya existe, no lo vuelve a crear ni le cambia la clave.

    Uso: python manage.py create_admin
    """

    help = 'Crea un superusuario desde variables de entorno (ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD).'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL', '')
        password = os.environ.get('ADMIN_PASSWORD')

        if not username or not password:
            self.stdout.write(
                'ADMIN_USERNAME / ADMIN_PASSWORD no configurados: se omite la creacion del superusuario.'
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True},
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado correctamente.'))
        else:
            self.stdout.write(f'El superusuario "{username}" ya existia, no se modifico.')