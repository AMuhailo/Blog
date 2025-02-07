from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class Topic(models.Model):
    title = models.CharField(max_length = 50)
    slug = models.SlugField(max_length = 250, blank = True)
    
    class Meta:
        ordering = ['-id']
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blogs:topic_post_list_view_url", kwargs={"topic_slug": self.slug,
                                                                 "topic_id":self.pk})
    
    
    def __str__(self):
        return self.title
    

class Post(models.Model):
    topic = models.ForeignKey("Topic",
                              verbose_name = "Topics", 
                              on_delete = models.CASCADE, 
                              related_name = 'post_topic')
    title = models.CharField(max_length = 50)
    slug = models.SlugField(max_length = 50 , blank = True)
    description = models.TextField(blank = True)
    author = models.ForeignKey(User, 
                               on_delete = models.CASCADE, 
                               related_name = 'creators')
    active = models.BooleanField(default = True)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='post_like')
    total_like = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blogs:post_detail_view_url", kwargs={"post_slug": self.slug,
                                                             "post_id":self.pk})

    def __str__(self):
        return self.title
    

class Content(models.Model):
    post = models.ForeignKey("Post", 
                             verbose_name = "Content", 
                             on_delete = models.CASCADE, 
                             related_name = 'content_post')
    content_ct = models.ForeignKey(ContentType,
                                   on_delete = models.CASCADE,
                                   related_name = 'content_objects',
                                   limit_choices_to={"model__in":('text','image','video')})
    content_id = models.PositiveIntegerField()
    contents = GenericForeignKey('content_ct', 'content_id')
    

class ItemContent(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name="%(class)s_content")
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]
        abstract = True
        

class Text(ItemContent):
    body = models.TextField()
class Image(ItemContent):
    image = models.FileField(upload_to = 'content/image/')
class Video(ItemContent):
    video = models.URLField()
    
    
class Comments(models.Model):
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = 'comments_post')
    message = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comment_author')
    
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields = ['created'])]
        
    def __str__(self):
        return f"Comments to post '{self.post}' with id {self.post.id}"
    