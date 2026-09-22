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
                    'Empecé a programar casi de casualidad. Sabía que quería estudiar algo '
                    'relacionado con tecnología y negocios —terminé el secundario en un colegio '
                    'germano-argentino con orientación en Economía y Administración—, pero nunca '
                    'había escrito una línea de código hasta que arranqué el curso de Python en '
                    'Coderhouse.\n\n'
                    'Las primeras clases fueron sobre tipos de datos, listas, tuplas, diccionarios '
                    'y sets. Al principio cuesta entender por qué hay tantas estructuras distintas '
                    'para guardar información, pero con la práctica se empieza a notar que cada una '
                    'sirve para un problema diferente: una lista para una colección ordenada que '
                    'puede repetir valores, un set cuando lo que importa es que no haya duplicados, '
                    'un diccionario cuando necesito buscar algo por una clave en vez de por '
                    'posición.\n\n'
                    'Después vinieron los condicionales, los bucles, las funciones y el manejo de '
                    'excepciones. Ahí fue cuando empecé a sentir que realmente podía "armar" algo, '
                    'no solo seguir ejercicios sueltos. Programar una función que valide datos, '
                    'calcule algo y devuelva un resultado prolijo se siente como resolver un '
                    'rompecabezas.\n\n'
                    'Más adelante llegó la programación orientada a objetos: clases, herencia, '
                    'encapsulamiento, polimorfismo. Esa parte me costó un poco más, pero fue clave '
                    'para entender cómo está construido Django por dentro, ya que todo el framework '
                    'se basa en clases (modelos, vistas, formularios). Hoy, mirando para atrás, '
                    'siento que pasé de no saber qué era una variable a poder armar una aplicación '
                    'web completa como este blog. Y esto recién empieza: la idea es seguir '
                    'profundizando en Python de cara a mi carrera en Wirtschaftsinformatik en TU '
                    'Berlin.'
                ),
            },
            {
                'title': 'Primeros pasos con Django',
                'category': 'Django',
                'summary': 'Una introducción práctica al framework MTV de Django.',
                'content': (
                    'Después de aprender las bases de Python, el curso de Coderhouse avanzó hacia '
                    'Django, un framework para construir aplicaciones web completas. La primera vez '
                    'que vi el patrón MTV (Modelo-Template-Vista, la versión de Django del clásico '
                    'MVC) me pareció bastante abstracto, pero se entiende rápido en la práctica: los '
                    'modelos definen qué datos guardo y cómo se relacionan entre sí, las vistas '
                    'deciden qué hacer con una solicitud del usuario, y los templates arman lo que '
                    'finalmente se ve en el navegador.\n\n'
                    'Lo primero que hice fue crear un proyecto y una app, y enseguida entendí una '
                    'idea central de Django: un proyecto puede tener varias apps, cada una '
                    'encargada de una parte del sistema. En este blog, por ejemplo, separamos la '
                    'lógica en tres apps: "blog" (publicaciones, categorías y comentarios), '
                    '"accounts" (registro, login y perfiles) y "pages" (inicio, "Acerca de" y '
                    'contacto). Esa separación ayuda mucho a mantener el código organizado a medida '
                    'que el proyecto crece.\n\n'
                    'Otro momento clave fue entender las migraciones: en vez de escribir SQL a mano '
                    'para crear tablas, defino los modelos en Python y Django genera '
                    'automáticamente los cambios necesarios en la base de datos con '
                    '"makemigrations" y "migrate". La primera vez que vi mis clases de Python '
                    'convertirse en tablas reales sin escribir una sola línea de SQL fue un quiebre '
                    'en cómo entendía el desarrollo web.\n\n'
                    'Ya avanzado el curso, aprendimos vistas basadas en clases (ListView, '
                    'DetailView, CreateView, UpdateView, DeleteView), que evitan repetir el mismo '
                    'código una y otra vez para operaciones típicas como listar, ver el detalle, '
                    'crear, editar o borrar un objeto. Y el panel de administración de Django '
                    'terminó de convencerme: con apenas unas líneas de configuración se obtiene una '
                    'interfaz completa para gestionar todo el contenido del sitio, algo que en '
                    'otros frameworks llevaría mucho más trabajo construir desde cero.'
                ),
            },
            {
                'title': 'Qué es el Fintech y por qué me interesa',
                'category': 'Fintech',
                'summary': 'Un repaso de las tecnologías financieras que están cambiando la industria.',
                'content': (
                    'Fintech es la combinación de "finanzas" y "tecnología": empresas y productos '
                    'que usan software para resolver problemas financieros de forma más rápida, '
                    'accesible y transparente que la banca tradicional. Pagos digitales, billeteras '
                    'virtuales, préstamos automatizados evaluados con algoritmos, inversión '
                    'accesible desde el celular, transferencias internacionales casi instantáneas: '
                    'todo eso es Fintech.\n\n'
                    'Me empezó a interesar el tema por una razón bastante concreta: terminé el '
                    'secundario con orientación en Economía y Administración, así que siempre tuve '
                    'un pie puesto en el mundo financiero. Pero a la vez me di cuenta de que lo que '
                    'más me entusiasmaba no era tanto la parte contable o de gestión tradicional, '
                    'sino pensar cómo la tecnología puede simplificar procesos que hoy son lentos, '
                    'caros o poco transparentes. Ahí es donde Fintech conecta perfecto con mi otro '
                    'gran interés: programar.\n\n'
                    'Una de las cosas que más me atrae de esta industria es lo interdisciplinaria '
                    'que es: no alcanza con saber programar, también hay que entender de '
                    'regulación financiera, de seguridad de la información, de experiencia de '
                    'usuario y de cómo se comportan las personas con su dinero. Es un campo donde '
                    'la tecnología no es un fin en sí mismo, sino una herramienta para resolver un '
                    'problema muy humano: que la gente pueda manejar su plata de forma más simple '
                    'y justa.\n\n'
                    'Por eso elegí orientar mi formación universitaria hacia Wirtschaftsinformatik '
                    '(informática de negocios) en TU Berlin: es exactamente la intersección entre '
                    'tecnología y economía que busco. Mi plan es seguir reforzando mis bases de '
                    'programación —este blog es parte de ese camino— mientras me preparo para '
                    'estudiar en Alemania, con la idea de, más adelante, trabajar en una empresa '
                    'Fintech o incluso animarme a desarrollar mi propio proyecto en esa industria.'
                ),
            },
            {
                'title': 'Mi camino hacia Wirtschaftsinformatik en TU Berlin',
                'category': 'Carrera y Estudios',
                'summary': 'Por qué elegí estudiar Wirtschaftsinformatik y cómo me estoy preparando.',
                'content': (
                    'Estudié toda mi educación secundaria en un colegio germano-argentino en '
                    'Buenos Aires, lo que significó cursar en alemán y en español desde chico y, '
                    'sobre el final, rendir el DSD II (un certificado oficial de alemán a nivel '
                    'B2/C1). Esa formación bilingüe —y ahora trilingüe, sumando inglés— fue la base '
                    'que me permitió plantearme en serio la idea de estudiar en Alemania.\n\n'
                    'Terminé el Bachillerato en Economía y Administración a fines de 2025, y desde '
                    'entonces empecé a preparar el camino hacia la universidad alemana. La carrera '
                    'que elegí es Wirtschaftsinformatik (informática de negocios) en la TU Berlin, '
                    'una combinación de ciencias de la computación, administración de empresas y '
                    'economía. Me atrae particularmente porque no tengo que elegir entre "ser '
                    'programador" o "trabajar en negocios": la carrera está pensada justamente para '
                    'formar profesionales que puedan moverse cómodos en las dos áreas, entendiendo '
                    'tanto el código como el contexto de negocio detrás de cada sistema.\n\n'
                    'Parte de mi preparación fue justamente este curso de Python en Coderhouse, y '
                    'este proyecto final —un blog completo hecho con Django, con registro de '
                    'usuarios, panel de administración, formularios validados y despliegue real— es '
                    'la forma que encontré de demostrarme a mí mismo (y a quien lo lea) que puedo '
                    'construir algo funcional de punta a punta, no solo entender la teoría.\n\n'
                    'El próximo paso en mi camino es rendir la documentación y trámites necesarios '
                    'para la aplicación a la universidad y organizar la mudanza a Berlín. Mientras '
                    'tanto, sigo reforzando mis conocimientos técnicos —Python, Django, y lo que '
                    'venga después— porque sé que cuanto más sólida sea esa base, mejor va a ser mi '
                    'punto de partida cuando arranque la carrera.'
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