from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),

    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('user/<str:username>/', UserProfileAPIView.as_view(), name='user-detail'),
    path('user/<str:username>/follow/', FollowAPIView.as_view(), name='follow'),
    path('user/<str:username>/followers/', UserFollowersAPIView.as_view(), name='followers'),
    path('user/<str:username>/following/', UserFollowingAPIView.as_view(), name='following'),
]
