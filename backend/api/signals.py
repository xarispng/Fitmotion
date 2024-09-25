from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Reschedules

@receiver(post_save, sender=User)
def create_user_reschedules(sender, instance, created, **kwargs):
    if created:
        Reschedules.objects.create(user=instance)