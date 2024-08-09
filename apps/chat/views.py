from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema

from apps.chat.models import Chat, Message, MessageRead
from apps.chat.serializers import ChatSerializer, ChatListSerializer, CreateGroupSerializer, ChatSettingSerializer


class ChatView(APIView):
    serializer_class = ChatListSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: ChatListSerializer(many=True)},
        tags=['Chat'],
        description='Get all chats'
    )
    def get(self, request):
        chats = Chat.objects.filter(participants=request.user, is_request=False).prefetch_related('participants')
        serializer = self.serializer_class(chats, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={201: ChatSerializer},
        tags=['Chat'],
        description='Create new chat'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatDetailView(APIView):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: ChatSerializer},
        tags=['Chat'],
        description='Get chat by id'
    )
    def get(self, request, chat_id):
        chat = get_object_or_404(
            Chat.objects.prefetch_related('messages', 'participants'),
            id=chat_id, participants=request.user
        )
        serializer = self.serializer_class(chat, context={'request': request})
        unread_messages = Message.objects.filter(chat=chat).exclude(read_by__user=request.user)
        for message in unread_messages:
            MessageRead.objects.create(message=message, user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateGroupView(APIView):
    serializer_class = CreateGroupSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={201: ChatSerializer},
        tags=['Chat'],
        description='Create new chat'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatSettingView(APIView):
    serializer_class = ChatSettingSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: ChatSettingSerializer},
        tags=['Chat'],
        description='Get chat setting'
    )
    def get(self, request):
        chat_settings = request.user.chat_settings
        serializer = self.serializer_class(chat_settings, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=ChatSettingSerializer,
        responses={200: ChatSettingSerializer},
        tags=['Chat'],
        description='Update chat setting'
    )
    def put(self, request):
        chat_settings = request.user.chat_settings
        serializer = self.serializer_class(chat_settings, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatRequestListView(APIView):
    serializer_class = ChatListSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: ChatListSerializer(many=True)},
        tags=['Chat Request'],
        description='Get all request chats'
    )
    def get(self, request):
        chats = Chat.objects.filter(participants=request.user, is_request=True).exclude(request_user=request.user).prefetch_related('participants')
        serializer = self.serializer_class(chats, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
