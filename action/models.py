from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Action(models.Model):
    user = models.ForeignKey('auth.User', on_delete = models.CASCADE, related_name = 'action_user')
    venv = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add = True)
    action_ct = models.ForeignKey(ContentType, on_delete = models.CASCADE, related_name = 'active_content_type', blank = True, null = True)
    action_id = models.PositiveIntegerField(blank = True, null = True)
    actions = GenericForeignKey('action_ct','action_id')
    
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields = ['-created'])]
    
    def __str__(self):
        return self.venv