from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('',views.PostListView.as_view(), name='post_list_view_url'),
    path('topic/<slug:topic_slug>/<int:topic_id>/',views.PostListView.as_view(), name = 'topic_post_list_view_url'),
    path('create/post/', views.PostCreateView.as_view(), name = 'post_create_view_url'),
    
    path('post/<slug:post_slug>/<int:post_id>/', views.PostDetailView.as_view(), name = 'post_detail_view_url'),
    path('post/<slug:post_slug>/<int:post_id>/update/', views.PostUpdateView.as_view(), name = 'post_update_view_url'),

    path('post/<int:post_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(), name='content_create_view_url'),
    path('post/<slug:post_slug>/<int:post_id>/comments/', views.PostCommentListView.as_view(), name = 'post_comment_list_view'),
    
    #Append parameters
    path('share/post/<slug:post_slug>/<int:post_id>/', views.share_post, name = 'share_post_url'),
    path('post/<int:post_id>/like/', views.like_post, name = 'like_post_url'),
]

