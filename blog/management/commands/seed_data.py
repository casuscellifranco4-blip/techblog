from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Profile
from blog.models import Category, Post

User = get_user_model()


class Command(BaseCommand):
    """Carga datos de ejemplo para poder probar y capturar pantallas de la app rápido.

    Uso: python manage.py seed_data
    """

    help = 'Carga categorías, un usuario de ejemplo y publicaciones de muestra.'

    def handle(self, *args, **options):
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@techblog.com'},
        )
        if created:
            demo_user.set_password('demo12345')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('Usuario demo creado -> usuario: demo / clave: demo12345'))
        else:
            self.stdout.write('El usuario demo ya existía, se reutiliza.')

        Profile.objects.get_or_create(
            user=demo_user,
            defaults={'bio': 'Cuenta de ejemplo para probar TechBlog.'},
        )

        categorias = ['Python', 'Django', 'Fintech', 'Carrera y Estudios']
        cat_objs = {}
        for nombre in categorias:
            cat, _ = Category.objects.get_or_create(name=nombre)
            cat_objs[nombre] = cat

        posts_demo = [
            {
                'title': 'Cómo empecé a programar en Python',
                'category': 'Python',
                'summary': 'Mi camino aprendiendo Python desde cero y los recursos que más me sirvieron.',
                'content': (
                    'Python es un lenguaje ideal para empezar en programación por su sintaxis '
                    'clara y su enorme comunidad. En este posteo cuento cómo fue mi proceso de '
                    'aprendizaje, desde los tipos de datos básicos hasta la programación orientada '
                    'a objetos, pasando por el manejo de archivos y excepciones.'
                ),
            },
            {
                'title': 'Primeros pasos con Django',
                'category': 'Django',
                'summary': 'Una introducción práctica al framework MTV de Django.',
                'content': (
                    'Django sigue el patrón Modelo-Template-Vista y permite construir aplicaciones '
                    'web robustas muy rápidamente. En este artículo repaso cómo crear modelos, '
                    'migrarlos a la base de datos, definir vistas basadas en clases y armar '
                    'templates reutilizables con herencia.'
                ),
            },
            {
                'title': 'Qué es el Fintech y por qué me interesa',
                'category': 'Fintech',
                'summary': 'Un repaso de las tecnologías financieras que están cambiando la industria.',
                'content': (
                    'El Fintech combina finanzas y tecnología para ofrecer productos financieros '
                    'más accesibles, rápidos y transparentes. Cuento por qué elegí orientar mi '
                    'carrera hacia esta industria y qué habilidades técnicas estoy desarrollando '
                    'para eso.'
                ),
            },
            {
                'title': 'Mi camino hacia Wirtschaftsinformatik en TU Berlin',
                'category': 'Carrera y Estudios',
                'summary': 'Por qué elegí estudiar Wirtschaftsinformatik y cómo me estoy preparando.',
                'content': (
                    'Después de terminar el secundario en un colegio germano-argentino, decidí '
                    'seguir mi formación en Alemania. En este posteo cuento el proceso de '
                    'preparación, desde el idioma hasta los conocimientos técnicos que quiero '
                    'reforzar antes de arrancar la carrera.'
                ),
            },
        ]

        creados = 0
        for data in posts_demo:
            _, was_created = Post.objects.get_or_create(
                title=data['title'],
                defaults={
                    'author': demo_user,
                    'category': cat_objs[data['category']],
                    'summary': data['summary'],
                    'content': data['content'],
                    'status': 'published',
                },
            )
            if was_created:
                creados += 1

        self.stdout.write(self.style.SUCCESS(
            f'Listo: {len(categorias)} categorías aseguradas, {creados} publicaciones nuevas creadas.'
        ))
