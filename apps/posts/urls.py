from django.urls import path

from apps.posts.views import PostAPIView, PostDetailAPIView, UserPostAPIView, LikeAPIView, SavePostAPIView, SavedPostAPIView

urlpatterns = [
    path('posts/my/', PostAPIView.as_view(), name='post-list'),
    path('posts/saved/', SavedPostAPIView.as_view(), name='post-saved'),
    path('posts/<int:post_id>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', LikeAPIView.as_view(), name='post-like'),
    path('posts/<int:post_id>/save/', SavePostAPIView.as_view(), name='post-save'),
    path('<str:username>/posts/', UserPostAPIView.as_view(), name='user-post-list'),
]
