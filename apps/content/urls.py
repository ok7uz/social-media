from django.urls import path

from apps.content.views import *


urlpatterns = [
    path('posts/', PostAPIView.as_view(), name='post-list'),
    path('discover/', DiscoverPostAPIView.as_view(), name='discover-posts'),
    path('posts/saved/', SavedPostAPIView.as_view(), name='post-saved'),
    path('posts/<int:post_id>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', LikeAPIView.as_view(), name='post-like'),
    path('posts/<int:post_id>/save/', SavePostAPIView.as_view(), name='post-save'),
    path('user/<str:username>/posts/', UserPostAPIView.as_view(), name='user-posts'),
    path('tags', TagListAPIView.as_view(), name='tag-list'),
]
