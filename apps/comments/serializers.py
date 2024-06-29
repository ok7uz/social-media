from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.accounts.serializers import UserListSerializer
from apps.posts.models import Post
from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'created_at', 'updated_at')

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
