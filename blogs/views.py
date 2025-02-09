from django.conf import settings
import redis
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.models import User
from django.forms.models import modelform_factory
from django.apps import apps
from action.utils import create_action
from django.core.mail import send_mail
from .tasks import send_message
from .models import Comments, Topic, Post, Content
from .forms import CommentPost, CreatePost, SharePost

# Create your views here.
if settings.REDIS_URL:
    r = redis.Redis.from_url(settings.REDIS_URL)
else:
    r = redis.Redis(settings.REDIS_HOST, port = settings.REDIS_PORT , db= settings.REDIS_DB)
    
    
try:
    r.ping()
    print("Redis connected.")
except redis.ConnectionError:
    print("Redis connected is a bad.")
    
class DashBoardListView(ListView):
    model = Post
    template_name = 'dashboard.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        posts = r.zrange('post_rang',0,-1,desc=True)[:10]
        posts_id = [int(id) for id in posts]
        self.most_view = list(Post.objects.filter(id__in = posts_id))
        self.most_view.sort(key=lambda x:posts_id.index(x.id))

        return self.model.objects.filter(active = True).select_related('author','author__profile','topic').prefetch_related('like_user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["most_view"] = self.most_view
        return context
        
    

class PostListView(ListView):
    model = Post
    template_name = 'pages/post_lists.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        posts = Post.objects.filter(active = True)\
                            .order_by('-total_like')\
                            .select_related('topic','author','author__profile')\
                            .prefetch_related('like_user')
        topic_slug = self.kwargs.get('topic_slug')
        topic_id = self.kwargs.get('topic_id')
        if topic_slug and topic_id:
            self.topic = get_object_or_404(Topic, 
                                           slug = topic_slug,
                                           id = topic_id)
            posts = posts.filter(topic=self.topic)\
                            .select_related('topic','author','author__profile')\
                            .prefetch_related('like_user')
        else:
            self.topic = None
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        return context



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePost
    template_name = 'forms/createpost.html'
    success_url = reverse_lazy('blogs:post_list_view_url')
    def form_valid(self, form):
        new_post = form.save(commit = False)
        new_post.author = self.request.user
        new_post.save()
        create_action(self.request.user, 'created post', new_post)
        return redirect('profile_detail_view_url', new_post.author)
    
    
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'pages/detail.html'
    def get_object(self, queryset = ...):
        queryset = self.model.objects.select_related('author','author__profile','topic')
        return get_object_or_404(queryset,
                                 slug = self.kwargs.get('post_slug'),
                                 id = self.kwargs.get('post_id'),
                                 active=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r_view = r.incrby(f'post:{self.get_object().id}:view', 1)
        r.zincrby('post_rang',1,self.get_object().id )
        context["form"] = CreatePost(instance=self.get_object())
        context['share_form'] = SharePost()
        context['comment_form'] = CommentPost()
        context['r_view'] = r_view
        return context
    
    
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    context_object_name = 'post'
    template_name = 'forms/createpost.html'
    fields = ['title', 'description']
    def get_object(self, queryset = ...):
        queryset = self.model.objects.select_related('author','author__profile','topic')
        return get_object_or_404(queryset,
                                 slug = self.kwargs.get('post_slug'),
                                 id = self.kwargs.get('post_id'))
    
    def form_valid(self, form):
        form.save()
        return render(self.request, 'pages/detail.html', {"post":self.get_object(),
                                                          'form': CreatePost(instance=self.get_object()),
                                                          'comment_form': CommentPost(),
                                                          'share_form': SharePost()})
    
    
    
class ContentCreateUpdateView(TemplateResponseMixin, View):
    posts = None
    model = None
    obj = None
    template_name = 'forms/createcontent.html'
    
    def get_form(self, model, *args, **kwargs ):
        Form = modelform_factory(model, exclude=['author','created','updated'])
        return Form(*args, **kwargs)
    
    def get_model(self, model_name):
        if model_name in ['text','image','video']:
            return apps.get_model(app_label = 'blogs',model_name = model_name)
        return None
    
    def dispatch(self, request, post_id, model_name, id = None):
        self.posts = get_object_or_404(Post, id = post_id, author = request.user)
        self.model = self.get_model(model_name) 
        if id:
            self.obj = get_object_or_404(self.model, id = id, author = request.user)
            
        return super().dispatch(request, post_id, model_name, id)

    def get(self, request, post_id, model_name, id = None):
        form = self.get_form(self.model, instance = self.obj)
        return self.render_to_response({'form_content':form,
                                        'object':self.obj,
                                        'post':self.posts})
        
    def post(self, request, post_id, model_name, id = None):
        form = self.get_form(self.model, 
                             instance = self.obj, 
                             files = request.FILES, 
                             data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            create_action(request.user, 'add content to', obj)

            if not id:
                Content.objects.create(post = self.posts,
                                       contents = obj)
            return redirect(self.posts.get_absolute_url())
        return self.render_to_response({'form_content':form,
                                        'object':self.obj,
                                        'post':self.posts})


class PostCommentListView(LoginRequiredMixin, CreateView):
    model = Comments 
    form_class = CommentPost
    template_name = 'forms/commentpost.html'
    def get_object(self, queryset = ...):
        return get_object_or_404(Post, slug = self.kwargs.get('post_slug'),
                                 id = self.kwargs.get('post_id'))
    def form_valid(self, form):
        comment = form.save(commit = False)
        comment.post = self.get_object()
        comment.author = self.request.user
        comment.save()
        comments = self.get_object().comments_post.select_related('post','author').all()
        return render(self.request,'pages/include/detail_comments.html',{"comments":comments})



@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, active=True)
    post_exists = post.like_user.filter(username=request.user.username).exists()
    if post.author != request.user:
        if post_exists:
            post.like_user.remove(request.user)
            create_action(request.user, 'liked', post)
        else:
            post.like_user.add(request.user)
    return render(request,'snippers/like.html',{"post":post})
        
        
        
@login_required
def share_post(request, post_slug, post_id):
    queryset = Post.objects.select_related('author','author__profile','topic')
    post = get_object_or_404(queryset, slug = post_slug, id = post_id)
    if request.method == 'POST':
        form = SharePost(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'Post about {post.title}'
            message = f'{cd['message']}\n'\
                    f"URL{post_url}"
            send_mail(subject,message,request.user.email, [cd['to']])
            return redirect(post.get_absolute_url())
    else:
        form = SharePost()
    context = {
        'post':post,
        'share_form':form,
    }
    return render(request,'forms/sharecontent.html', context)
