from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.serializers import UserListSerializer
from apps.content.models import Post, Like, SavedPost, Tag
from apps.content_plan.models import ContentPlan
from config.utils import TimestampField


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    tag_list = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    tagged_user_list = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    content_plan_id = serializers.IntegerField(source='content_plan.id', write_only=True, required=False)
    tags = TagSerializer(many=True, read_only=True)
    user = UserListSerializer(read_only=True)
    has_liked = serializers.SerializerMethodField()
    has_saved = serializers.SerializerMethodField()
    created_at = TimestampField(read_only=True)
    updated_at = TimestampField(read_only=True)
    tagged_users = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'caption', 'comment_count', 'like_count', 'has_liked', 'tagged_user_list',
            'has_saved', 'created_at', 'updated_at', 'media', 'tag_list', 'tags', 'tagged_users', 'content_plan_id'
        )

    def get_has_liked(self, obj) -> bool:
        user = self.context.get('request').user
        return Like.objects.filter(post=obj, user=user).exists()

    def get_has_saved(self, obj) -> bool:
        user = self.context.get('request').user
        return SavedPost.objects.filter(post=obj, user=user).exists()

    def create(self, validated_data):
        tags = validated_data.pop('tag_list', [])
        tagged_users = validated_data.pop('tagged_user_list', [])
        content_plan = validated_data.pop('content_plan', None)
        if content_plan:
            validated_data['content_plan'] = get_object_or_404(ContentPlan, id=content_plan['id'])
        post = Post.objects.create(**validated_data)
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)
        for username in tagged_users:
            user = get_object_or_404(User, username=username)
            post.tagged_users.add(user)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_list', None)
        tagged_users = validated_data.pop('tagged_user_list', None)

        # Complete this part

        # content_plan = validated_data.pop('content_plan', instance.content_plan)
        # content_plan = get_object_or_404(ContentPlan, id=content_plan_id)
        # validated_data['content_plan'] = content_plan

        if tags:
            instance.tags.clear()
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
        if tagged_users:
            instance.tagged_users.clear()
            for username in tagged_users:
                user = get_object_or_404(User, username=username)
                instance.tagged_users.add(user)
        return super().update(instance, validated_data)

    @staticmethod
    def validate_media(value):
        content_type = value.content_type.split('/')[0]
        max_size = 200 * 1024 * 1024  # 200 MB

        if content_type not in ['image', 'video']:
            raise ValidationError("Unsupported file type. Allowed types are: jpg, png, mp4.")
        if value.size > max_size:
            raise ValidationError(f"File size must be less than {max_size // (1024 * 1024)} MB.")
        return value


class PostWithoutUserSerializer(PostSerializer):
    created_at = TimestampField(read_only=True)
    updated_at = TimestampField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'caption', 'media', 'tags', 'like_count',
            'comment_count', 'created_at', 'updated_at'
        )
            

class SavedPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedPost
        fields = ('post', 'user')
