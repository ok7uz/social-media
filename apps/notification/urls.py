from django.urls import path

from apps.notification.views import NotificationView, SaveFCMDeviceView

urlpatterns = [
    path('notifications/', NotificationView.as_view()),
    path('fcm-devices/', SaveFCMDeviceView.as_view()),
]
