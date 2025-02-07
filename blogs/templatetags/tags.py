from django import template
from django.shortcuts import get_object_or_404
from blogs.models import Topic, Post
from django.db.models import Count
from action.models import Action
from blogs.forms import CreatePost

register = template.Library()
    
@register.simple_tag()
def topics_tag():
    return Topic.objects.all()


@register.inclusion_tag("pages\include\detail_similar.html")
def similar_tag(post):
    similar_posts = post.topic.post_topic.select_related('author','author__profile').exclude(id=post.id).filter(active=True)[:8]
    return {"similar_posts":similar_posts}


@register.inclusion_tag('pages/include/detail_comments.html')
def comments_tag(post):
    comments = post.comments_post.select_related('post','author').all()
    return {"comments":comments} 


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
    
    
@register.simple_tag
def likes_tag(user):
    liked_posts = user.post_like.filter(active=True)[:8]
    return liked_posts


@register.inclusion_tag('registration/include/user-post.html')
def creators_tag(user):
    posts = user.creators.all().select_related('author','author__profile','topic').order_by("-total_like").prefetch_related('like_user')
    form = CreatePost()
    return {"posts":posts, 'form':form}


@register.inclusion_tag('pages/include/detail_content.html')
def contents_tag(post):
    contents = post.content_post.all().select_related('post','content_ct').prefetch_related('contents')
    return {"contents":contents}


@register.inclusion_tag('include/followerbar.html')
def follower_tag(user):
    following = user.following.all().select_related('profile').prefetch_related('followers','following')
    return {"following":following, "user":user}

@register.inclusion_tag('snippers/action.html')
def actions_tag(user_now):
    actions = Action.objects.exclude(user = user_now)
    following_ids = user_now.following.values_list('id',flat=True) 
    if following_ids:
        actions = actions.filter(user_id__in = following_ids)
    actions = actions[:5].select_related('user','user__profile').prefetch_related('actions')
    return {"actions":actions}