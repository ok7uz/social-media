from rest_framework import serializers

from apps.accounts.serializers import UserListSerializer
from apps.posts.models import Post, Like, SavedPost, Media, Tag


class MediaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Media
        fields = ('id', 'image', 'video')
        
        
class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    tag_list = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    tags = TagSerializer(many=True, read_only=True)
    user = UserListSerializer(read_only=True)
    media = MediaSerializer(many=True, required=False)
    has_liked = serializers.SerializerMethodField()
    has_saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'caption', 'media', 'tag_list', 'tags', 'comment_count',
            'like_count', 'has_liked', 'has_saved', 'created_at', 'updated_at'
        )

    def get_has_liked(self, obj) -> bool:
        user = self.context.get('request').user
        return Like.objects.filter(post=obj, user=user).exists()

    def get_has_saved(self, obj) -> bool:
        user = self.context.get('request').user
        return SavedPost.objects.filter(post=obj, user=user).exists()

    def create(self, validated_data):
        tags = validated_data.pop('tag_list', [])
        media = validated_data.pop('media')
        post = Post.objects.create(**validated_data)
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)
        media_serializer = MediaSerializer(data=media, many=True, context=self.context)
        media_serializer.is_valid()
        media_serializer.save(post=post)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_list', list(instance.tags.all().values_list('name', flat=True)))
        instance.tags.clear()
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)
        return super().update(instance, validated_data)


class PostWithoutUserSerializer(PostSerializer):

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
