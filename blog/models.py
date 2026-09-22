from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Categoría temática de las publicaciones (Python, Django, Fintech, etc.)."""

    name = models.CharField('nombre', max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Entrada del blog."""

    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
    ]

    title = models.CharField(
        'título',
        max_length=200,
        validators=[MinLengthValidator(5, 'El título debe tener al menos 5 caracteres.')],
    )
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='autor',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='categoría',
    )
    summary = models.CharField(
        'resumen',
        max_length=300,
        help_text='Breve descripción que aparece en el listado (máx. 300 caracteres).',
    )
    content = models.TextField(
        'contenido',
        validators=[MinLengthValidator(20, 'El contenido debe tener al menos 20 caracteres.')],
    )
    image = models.ImageField('imagen', upload_to='posts/%Y/%m/', blank=True, null=True)
    status = models.CharField('estado', max_length=10, choices=STATUS_CHOICES, default='published')
    created_at = models.DateTimeField('creado', auto_now_add=True)
    updated_at = models.DateTimeField('actualizado', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'

    def __str__(self):
        return self.title

    def clean(self):
        """Validación a nivel de modelo: una publicación marcada como
        'publicada' siempre debe tener un resumen cargado, para que se vea
        bien en el listado del blog."""
        if self.status == 'published' and not self.summary.strip():
            raise ValidationError(
                {'summary': 'Las publicaciones publicadas deben tener un resumen.'}
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f'{base_slug}-{counter}'
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    """Comentario de un usuario autenticado en una publicación."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='publicación')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='autor',
    )
    content = models.TextField('comentario', max_length=1000)
    created_at = models.DateTimeField('creado', auto_now_add=True)
    active = models.BooleanField('activo', default=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'Comentario de {self.author} en "{self.post}"'
