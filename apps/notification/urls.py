from django.urls import path

from apps.notification.views import NotificationView, SaveFCMTokenView

urlpatterns = [
    path('notifications/', NotificationView.as_view()),
    path('fcm-tokens/', SaveFCMTokenView.as_view()),
]
