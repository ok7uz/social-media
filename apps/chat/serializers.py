from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema_field

from config.utils import TimestampField
from .models import Chat, Message
from apps.accounts.models import User, Follow
from apps.accounts.serializers import UserListSerializer
from apps.content_plan.models import Subscription, ContentPlan


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(read_only=True, source='sender.username')
    created_at = TimestampField(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender_username', 'content', 'media', 'media_type', 'created_at']


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserListSerializer(many=True, read_only=True)
    owner = UserListSerializer(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    created_at = TimestampField(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'image', 'owner', 'participants', 'is_group', 'created_at', 'messages']

    def get_name(self, obj) -> str:
        if obj.is_group:
            return obj.name
        user = self.context['request'].user
        participant = obj.participants.exclude(id=user.id).first()
        if participant.last_name:
            return f'{participant.first_name} {participant.last_name}'
        return participant.first_name

    @extend_schema_field(serializers.URLField())
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.is_group:
            return request.build_absolute_uri(obj.image.url) if obj.image else None
        user = self.context['request'].user
        participant = obj.participants.exclude(id=user.id).first()
        if participant.profile_picture:
            return request.build_absolute_uri(participant.profile_picture.url)
        return None


class ChatListSerializer(ChatSerializer):
    TYPE = [
        ('superhero', 'Superhero'),
        ('subscriber', 'Subscriber'),
        ('follower', 'Follower'),
        ('group', 'Group'),
    ]
    username = serializers.CharField(write_only=True, help_text='Username of the participant')
    type = serializers.SerializerMethodField(read_only=True)
    last_message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'is_group', 'username', 'type', 'name', 'image', 'last_message', 'created_at']

    def create(self, validated_data):
        username = validated_data.pop('username')
        participant_user = get_object_or_404(User, username=username)
        chat = Chat.objects.create(name='testing')
        chat.participants.add(participant_user, self.context['request'].user)
        return chat

    @extend_schema_field(serializers.ChoiceField(choices=TYPE))
    def get_type(self, obj) -> str:
        if obj.is_group:
            return 'group'
        user = self.context['request'].user
        participant = obj.participants.exclude(id=user.id).first()
        if Subscription.objects.filter(user=user, content_plan__user=participant).exists():
            return 'superhero'
        elif Subscription.objects.filter(user=participant, content_plan__user=user).exists():
            return 'subscriber'
        elif Follow.objects.filter(follower=participant, following=user).exists():
            return 'follower'
        return None

    @extend_schema_field(MessageSerializer())
    def get_last_message(self, obj) -> str:
        _last_message = obj.messages.last()
        serializer = MessageSerializer(obj.messages.last(), context=self.context)
        return serializer.data if _last_message else None


class CreateGroupSerializer(ChatSerializer):
    group_name = serializers.CharField(write_only=True, required=False)
    group_image = serializers.ImageField(write_only=True, required=False)
    content_plan_id = serializers.IntegerField(write_only=True, required=False)
    user_id_list = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = Chat
        fields = [
            'id', 'group_name', 'group_image', 'content_plan_id', 'user_id_list', 'name', 'image', 'owner',
            'participants', 'is_group', 'created_at',
        ]

    def create(self, validated_data):
        group_name = validated_data.pop('group_name', None)
        group_image = validated_data.pop('group_image', None)
        content_plan_id = validated_data.pop('content_plan_id', None)
        user_id_list = validated_data.pop('user_id_list', [])
        chat = Chat.objects.create(name=group_name, image=group_image, is_group=True, owner=self.context['request'].user)
        chat.participants.add(self.context['request'].user)
        for user_id in user_id_list:
            user = get_object_or_404(User, id=user_id)
            chat.participants.add(user)
        if content_plan_id:
            content_plan = get_object_or_404(ContentPlan, id=content_plan_id)
            plan_users = User.objects.filter(subscription__content_plan=content_plan)
            for user in plan_users:
                if not chat.participants.filter(id=user.id).exists():
                    chat.participants.add(user)
        return chat
