from django.views.generic import FormView, DetailView, ListView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from action.utils import create_action
from blogs.forms import CreatePost
from .models import Followers, Profile
from .forms import RegisterForm, ProfileEditForm, UserDataEditForm

# Create your views here.
class RegisterUser(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = 'login'
    
    def form_valid(self, form):
        cd = form.cleaned_data
        new_user = form.save(commit = False)
        new_user.set_password(cd['password'])
        new_user.save()
        create_action(new_user,'registration')
        return super().form_valid(form)

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'registration/profile/user-list.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return self.model.objects.filter(is_active = True).select_related('profile').prefetch_related('followers').exclude(username=self.request.user.username)
    

class ProfileDetailView(DetailView):
    model = User
    template_name = 'registration/profile/profile.html'
    context_object_name = 'user'
    
    def get_object(self, queryset = ...):
        queryset = self.model.objects.select_related('profile','profile__user').prefetch_related('followers','following')
        return get_object_or_404(queryset, 
                                 username = self.kwargs.get('username'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreatePost()
        return context
    
class FollowingDetailView(ListView):
    model = User
    template_name = 'registration/profile/followers-list.html'
    context_object_name = 'follow_post'
    
    def get_queryset(self):
        queryset = User.objects.select_related('profile','profile__user')\
                                .prefetch_related('followers','following')
        self.user = get_object_or_404(queryset, 
                                 username = self.kwargs.get('username'))
        follow_id = self.kwargs.get('follow_id')
        follow_post = self.user.creators.all()
        if follow_id:
            self.follow_user = self.user.following.get(id=follow_id)
            follow_post = self.follow_user.creators.filter(author=self.follow_user)
        else:
            self.follow_user = None 
        return follow_post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['follow_user'] = self.follow_user
        context['user'] = self.user
        return context
    
@login_required
def profile_edit(request):
    if request.method == "POST":
        user_form = UserDataEditForm(instance = request.user,data = request.POST )
        profile_form = ProfileEditForm(instance = request.user.profile, data = request.POST,  files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_detail_view_url', request.user)
    else:
        user_form = UserDataEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request,'registration/profile/editprofile.html',context)

@login_required
def followed(request,user_id):
    user = get_object_or_404(User,pk = user_id)
    follow_user = user.followers.filter(username = request.user.username).exists()
    if request.user != user:
        try:
            if not follow_user:
                Followers.objects.get_or_create(from_user = request.user, to_user = user)
                create_action(request.user , 'followers', user )
            else:
                Followers.objects.filter(from_user = request.user, to_user = user).delete()
        except User.DoesNotExist:
            return None
    return HttpResponse(user.followers.count() )


def sing_in_username(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    if  User.objects.filter(email = email).exists():
        return HttpResponse("<div id='sing-in-username' class='text-danger'>Account exists! Please log-in.</div>")
    elif User.objects.filter(username = username,email = email).exists():
        return HttpResponse("<div id='sing-in-username' class='text-danger'>Account exists! Please log-in.</div>")
    else:
        return HttpResponse("<div id='sing-in-username' class='text-success'>This username is available!</div>")