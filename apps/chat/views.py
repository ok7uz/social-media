from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema

from apps.chat.models import Chat
from apps.chat.serializers import ChatSerializer, ChatListSerializer


class ChatView(APIView):
    serializer_class = ChatListSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: ChatListSerializer},
        tags=['Chat'],
        description='Get all chats'
    )
    def get(self, request):
        chats = Chat.objects.filter(participants=request.user)
        serializer = self.serializer_class(chats, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatDetailView(APIView):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: ChatSerializer},
        tags=['Chat'],
        description='Get chat by id'
    )
    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
        serializer = self.serializer_class(chat, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
