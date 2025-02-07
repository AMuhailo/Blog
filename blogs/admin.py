from django.contrib import admin
from .models import Topic, Post, Content, Comments
# Register your models here.

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug':('title',)}
    
    
class ContentInLine(admin.StackedInline):
    model = Content
    fields = ['post','content_ct','content_id']
    
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['topic','title','author','created','updated','active']
    list_filter = ['topic','author','created','updated']
    search_fields = ['title','description']
    list_editable = ['title','active']
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'created'
    inlines = [ContentInLine]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['post','created','updated']
    list_filter = ['created']
    search_fields = ['message']
    date_hierarchy = 'created'