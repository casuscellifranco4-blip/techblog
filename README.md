# TechBlog

Aplicación web de blog desarrollada con **Django**, como proyecto final del
curso de Python de Coderhouse. Permite a los usuarios registrarse, crear y
editar publicaciones sobre programación y tecnología, comentar publicaciones
de otros usuarios, y gestionar su propio perfil.

## Índice

- [Descripción del proyecto](#descripción-del-proyecto)
- [Funcionalidades principales](#funcionalidades-principales)
- [Tecnologías](#tecnologías)
- [Instalación y ejecución local](#instalación-y-ejecución-local)
- [Datos de ejemplo](#datos-de-ejemplo)
- [Despliegue en Render](#despliegue-en-render)
- [Estructura del proyecto](#estructura-del-proyecto)

## Descripción del proyecto

**Propósito:** ofrecer una plataforma simple donde compartir y leer
artículos sobre programación, Django, Fintech y desarrollo de carrera en
tecnología.

**Problema que resuelve:** los blogs genéricos no permiten una gestión
sencilla de contenido con control de autoría, moderación de comentarios y
un panel administrativo propio. TechBlog resuelve esto ofreciendo:

- un panel de administración completo para gestionar publicaciones,
  categorías, comentarios y usuarios;
- un sistema de cuentas donde cada usuario gestiona sus propias
  publicaciones y su perfil;
- formularios con validaciones que garantizan la integridad del contenido.

**Tipo de usuario:** cualquier persona interesada en tecnología que quiera
leer artículos, comentar, o registrarse para publicar los suyos.

## Funcionalidades principales

- **Panel de administración (Django Admin):** gestión de categorías,
  publicaciones (con filtros por estado/categoría/fecha y búsqueda) y
  comentarios (con acciones para aprobar/desactivar en lote).
- **Registro y perfiles de usuario:** registro con usuario, email y
  contraseña (con validaciones), inicio y cierre de sesión, y edición de
  perfil (biografía, foto, sitio web, ubicación).
- **Páginas funcionales:** inicio con las últimas publicaciones, listado de
  blog con búsqueda y filtro por categoría, detalle de publicación con
  comentarios, página "Acerca de" y formulario de contacto.
- **Formularios con validación:** creación/edición de publicaciones
  (longitud mínima de título y contenido), comentarios, registro de
  usuario (email único) y contacto (longitud mínima del mensaje).
- **Control de permisos:** solo el autor de una publicación puede
  editarla o eliminarla; solo usuarios autenticados pueden publicar o
  comentar.

## Tecnologías

- Python 3 + Django 4.2 (LTS)
- SQLite en desarrollo / PostgreSQL en producción (vía `dj-database-url`)
- Bootstrap 5 (CDN) para la interfaz
- WhiteNoise para servir archivos estáticos en producción
- Gunicorn como servidor de aplicación en producción
- Render como plataforma de despliegue

## Instalación y ejecución local

### Requisitos previos

- Python 3.10 o superior instalado
- `pip` (viene con Python)
- Git

### Pasos

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/TU-USUARIO/techblog.git
   cd techblog
   ```

2. **Crear y activar un entorno virtual**

   ```bash
   python3 -m venv venv

   # En Linux / macOS:
   source venv/bin/activate

   # En Windows (PowerShell):
   venv\Scripts\Activate.ps1
   ```

3. **Instalar las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno**

   ```bash
   cp .env.example .env
   ```

   El archivo `.env.example` ya trae valores por defecto que funcionan en
   local (SQLite, `DEBUG=True`). No es necesario modificarlo para probar
   el proyecto localmente.

5. **Aplicar las migraciones**

   ```bash
   python manage.py migrate
   ```

6. **Crear un superusuario** (para acceder al panel de administración)

   ```bash
   python manage.py createsuperuser
   ```

7. **(Opcional) Cargar datos de ejemplo** — categorías y publicaciones de
   muestra, útiles para probar la app y sacar capturas de pantalla sin
   cargar todo a mano:

   ```bash
   python manage.py seed_data
   ```

8. **Ejecutar el servidor de desarrollo**

   ```bash
   python manage.py runserver
   ```

9. **Abrir la aplicación**

   - Sitio: <http://127.0.0.1:8000/>
   - Panel de administración: <http://127.0.0.1:8000/admin/>

## Datos de ejemplo

El comando `python manage.py seed_data` crea:

- 4 categorías (Python, Django, Fintech, Carrera y Estudios)
- Un usuario de ejemplo (`demo` / `demo12345`)
- 4 publicaciones de muestra publicadas

Se puede ejecutar las veces que sea necesario: no duplica los datos si ya
existen.

## Despliegue en Render

El proyecto ya incluye todo lo necesario para desplegarse en
[Render](https://render.com) (plan gratuito):

- `build.sh`: instala dependencias, ejecuta `collectstatic` y aplica las
  migraciones en cada despliegue.
- `Procfile` / `startCommand`: `gunicorn techblog.wsgi:application`
- `render.yaml`: blueprint para crear el Web Service y la base de datos
  PostgreSQL automáticamente.
- Configuración de `ALLOWED_HOSTS`, archivos estáticos (WhiteNoise) y
  base de datos (`dj-database-url`) mediante variables de entorno.

### Pasos para desplegar

1. Subí el proyecto a un repositorio público de GitHub (ver más abajo).
2. Entrá a [dashboard.render.com](https://dashboard.render.com) y creá una
   cuenta gratuita (podés usar tu cuenta de GitHub).
3. **New +** → **Blueprint** → conectá tu repositorio. Render va a leer
   `render.yaml` automáticamente y va a proponer crear:
   - un **Web Service** llamado `techblog`
   - una base de datos **PostgreSQL** llamada `techblog-db`
4. Confirmá la creación. Render instala las dependencias, corre
   `collectstatic` y las migraciones (`build.sh`), y levanta el servidor.
5. Cuando termine el build, Render te da una URL pública del estilo
   `https://techblog-XXXX.onrender.com`.
6. Entrá a esa URL, y para crear un superusuario en producción usá la
   consola de Render (**Shell** en el dashboard del Web Service):

   ```bash
   python manage.py createsuperuser
   ```

**Alternativa manual (sin Blueprint):** si preferís no usar `render.yaml`,
podés crear el Web Service a mano en el dashboard indicando:
- Build Command: `./build.sh`
- Start Command: `gunicorn techblog.wsgi:application`
- Variables de entorno: `SECRET_KEY` (generada), `DEBUG=False`,
  `ALLOWED_HOSTS=.onrender.com`, y `DATABASE_URL` (la de la base de datos
  PostgreSQL que crees en Render).

> **Nota sobre almacenamiento de archivos:** el plan gratuito de Render no
> tiene disco persistente, por lo que las imágenes subidas a través de la
> app (posts o avatares) se pierden en cada redeploy. Para un uso real en
> producción se recomienda un servicio de almacenamiento externo (por
> ejemplo Cloudinary o Amazon S3); queda fuera del alcance de este
> proyecto académico.

## Estructura del proyecto

```
techblog/
├── manage.py
├── requirements.txt
├── build.sh
├── Procfile
├── render.yaml
├── .env.example
├── techblog/          # configuración del proyecto (settings, urls)
├── blog/               # publicaciones, categorías, comentarios
│   └── management/commands/seed_data.py
├── accounts/           # registro, login, perfiles de usuario
├── pages/               # inicio, acerca de, contacto
├── templates/           # templates HTML (herencia de base.html)
├── static/css/          # estilos propios
└── media/                # imágenes subidas por los usuarios
```

---

Proyecto desarrollado por **Franco Casuscelli** como entrega final del
curso de Python — Coderhouse.
