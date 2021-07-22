from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import update_activities_distances

from .models import (
    School
)


@receiver(post_save, sender=School)
def update_user_profile(sender, instance, created, **kwargs):

    if created:
        update_activities_distances.delay(instance)
