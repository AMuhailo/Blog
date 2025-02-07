from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save,sender = User)
def profile_pre_save(sender, instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)