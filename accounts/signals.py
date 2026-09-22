from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Crea automáticamente un Profile cada vez que se crea un User nuevo
    (incluyendo el que crea `createsuperuser`)."""
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
