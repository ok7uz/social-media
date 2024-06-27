from django.urls import path

from .views import LoginAPIView, RegisterAPIView, ProfileAPIView

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/profile/', ProfileAPIView.as_view(), name='user-detail'),
    path('api/profile/<str:username>/', ProfileAPIView.as_view(), name='user-detail'),
]
