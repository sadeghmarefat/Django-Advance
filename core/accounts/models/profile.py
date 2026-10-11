from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .user import User


class Profile(models.Model):
    '''Model representing a user profile.'''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
