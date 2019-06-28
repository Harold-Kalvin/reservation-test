from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    """Model for a profile which is linked to a user and contains a timezone."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(_("Timezone"), max_length=255, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal to create a profile when a user is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Signal to save the profile of an updated user."""
    instance.profile.save()
