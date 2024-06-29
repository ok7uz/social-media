from rest_framework import serializers

from apps.accounts.serializers import UserListSerializer
from apps.posts.models import Post, Like, SavedPost


class PostSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    tags = serializers.ListSerializer(child=serializers.CharField(max_length=255), required=False)
    liked = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'title', 'content', 'image', 'tags', 'comments_count',
            'likes_count', 'liked', 'saved', 'created_at', 'updated_at'
        )

    def get_liked(self, obj) -> bool:
        user = self.context.get('request').user
        return Like.objects.filter(post=obj, user=user).exists()

    def get_saved(self, obj) -> bool:
        user = self.context.get('request').user
        return SavedPost.objects.filter(post=obj, user=user).exists()

    def create(self, validated_data):
        tags = validated_data.pop('tags') if 'tags' in validated_data else None
        post = Post.objects.create(**validated_data)
        post.add_tags(tags) if tags else None
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags') if 'tags' in validated_data else None
        instance.add_tags(tags) if tags else None
        return super().update(instance, validated_data)


class PostWithoutUserSerializer(PostSerializer):

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'content', 'image', 'tags', 'likes_count',
            'comments_count', 'created_at', 'updated_at'
        )
            

class SavedPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedPost
        fields = ('post', 'user')
