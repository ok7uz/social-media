from django.urls import path

from apps.content.views import *


urlpatterns = [
    path('contents/', ContentAPIView.as_view(), name='content-list'),
    path('discover/', DiscoverContentAPIView.as_view(), name='discover-contents'),
    path('contents/saved/', SavedContentAPIView.as_view(), name='content-saved'),
    path('contents/<int:content_id>/', ContentDetailAPIView.as_view(), name='content-detail'),
    path('contents/<int:content_id>/like/', LikeAPIView.as_view(), name='content-like'),
    path('contents/<int:content_id>/save/', SaveContentAPIView.as_view(), name='content-save'),
    path('user/<str:username>/contents/', UserContentAPIView.as_view(), name='user-contents'),
    path('tags', TagListAPIView.as_view(), name='tag-list'),
]
