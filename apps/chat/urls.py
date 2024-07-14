from django.urls import path

from apps.chat.views import ChatView

urlpatterns = [
    path('chats/', ChatView.as_view(), name='chats'),
]
