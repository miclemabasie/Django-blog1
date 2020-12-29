from django.urls import path
from . import views
from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    path('feed/', LatestPostFeed(), name='post_feed'),
    # path('', views.home, name='home'),
    path('', views.list_post, name='post_list'),
    path('<slug:slug>', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.list_post, name='post_list_by_tag'),
    # path('', views.PostList.as_view(), name='post_list'),
    path('<int:id>/share/', views.share_post, name='share_post'),
    path('search/', views.post_search, name='post_search'),
    
    
]