from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .serializers import CommentSerializer
from apps.comments.models import Comment
from apps.posts.models import Post


class CommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: CommentSerializer},
        tags=['comment'],
        description='Get all comments for post'
    )
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @extend_schema(
        request=CommentSerializer,
        responses={201: CommentSerializer},
        tags=['comment'],
        description='Create new comment'
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
