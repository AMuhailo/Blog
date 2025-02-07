from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'profile/', null = True, blank = True)
    birthday = models.DateField(blank = True, null = True)
    
    def __str__(self):
        return f"Profile {self.id}"

class Followers(models.Model):
    from_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='user_from')
    to_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='to_user')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
user_model = get_user_model()
user_model.add_to_class('following',models.ManyToManyField('self',
                                                           through=Followers,
                                                           symmetrical=False,
                                                           related_name='followers'))