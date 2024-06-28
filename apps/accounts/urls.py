from django.urls import path

from .views import LoginAPIView, RegisterAPIView, ProfileAPIView, UserProfileAPIView, FollowAPIView, \
    UserFollowingAPIView, UserFollowersAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/<str:username>/', UserProfileAPIView.as_view(), name='user-detail'),
    path('<str:username>/follow/', FollowAPIView.as_view(), name='user-follow'),
    path('<str:username>/followers/', UserFollowersAPIView.as_view(), name='user-followers'),
    path('<str:username>/following/', UserFollowingAPIView.as_view(), name='user-following'),
]
