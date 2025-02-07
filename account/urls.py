from django.urls import path
from . import views

urlpatterns = [
    path('sing-in/', views.RegisterUser.as_view(), name = 'register_user_url'),
    path('users/',views.UserListView.as_view(), name = 'user_list_view'),
    path('profile/<username>/', views.ProfileDetailView.as_view(), name = 'profile_detail_view_url'),
    path('profile/<username>/followers/', views.FollowingDetailView.as_view(), name = 'following_detail_view_url'),
    path('profile/<username>/followers/<follow_id>/', views.FollowingDetailView.as_view(), name = 'following_post_view_url'),
    path('user/edit/', views.profile_edit, name='profile_edit_url'),
    path('follow/<user_id>/', views.followed, name='followed_url'),
]

htmx = [
    path('sing-in-username/', views.sing_in_username, name = 'sing-in-username'),
]

urlpatterns += htmx