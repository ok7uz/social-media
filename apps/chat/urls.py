from django.urls import path

from apps.chat.views import ChatView, ChatDetailView, CreateGroupView

urlpatterns = [
    path('chats/', ChatView.as_view(), name='chat-list'),
    path('chats/<int:chat_id>/', ChatDetailView.as_view(), name='chat-detail'),
    path('chats/create-group/', CreateGroupView.as_view(), name='create-group'),
]
