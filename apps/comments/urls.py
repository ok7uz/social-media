from django.urls import path

from apps.comments.views import CommentAPIView

urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentAPIView.as_view(), name='comment'),
]
