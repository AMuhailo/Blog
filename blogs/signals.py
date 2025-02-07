from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post

@receiver(m2m_changed, sender=Post.like_user.through)
def like(sender, instance,**kwargs):
    instance.total_like = instance.like_user.count()
    instance.save()