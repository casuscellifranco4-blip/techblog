from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Perfil extendido de cada usuario registrado."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    bio = models.TextField('biografía', max_length=500, blank=True)
    avatar = models.ImageField('foto de perfil', upload_to='avatars/', blank=True, null=True)
    website = models.URLField('sitio web', blank=True)
    location = models.CharField('ubicación', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'Perfil de {self.user.username}'
