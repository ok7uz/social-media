from rest_framework import serializers
from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'timestamp']


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'participants', 'is_group', 'created_at', 'messages']


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'is_group', 'created_at']
