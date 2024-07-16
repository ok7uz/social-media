from drf_spectacular.utils import extend_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.content.models import Post, Like, SavedPost, Tag
from apps.content.serializers import PostSerializer, PostWithoutUserSerializer, TagSerializer


class PostAPIView(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: PostSerializer(many=True)},
        tags=['Post'],
        description='Get recommended posts'
    )
    def get(self, request):
        user = request.user
        followed_users = User.objects.filter(followers__follower=user)
        recommended_posts = Post.objects.filter(user__in=followed_users)
        recommended_posts = recommended_posts.select_related('user').prefetch_related('tags', 'tagged_users')
        serializer = PostSerializer(recommended_posts, many=True, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        request=PostSerializer,
        responses={201: PostSerializer},
        tags=['Post'],
        description='Create new post'
    )
    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PostDetailAPIView(APIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: PostSerializer},
        tags=['Post'],
        description='Get post info'
    )
    def get(self, request, post_id):
        post = get_object_or_404(
            Post.objects.select_related('user').prefetch_related('tags', 'tagged_users'),
            id=post_id
        )
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        request=PostSerializer,
        responses={200: PostSerializer},
        tags=['Post'],
        description='Update post info'
    )
    def put(self, request, post_id):
        post = get_object_or_404(
            Post.objects.select_related('user').prefetch_related('tags', 'tagged_users'),
            id=post_id
        )
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        responses={204: None},
        tags=['Post'],
        description='Delete post'
    )
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=204)


class UserPostAPIView(APIView):
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: PostSerializer(many=True)},
        tags=['User'],
        description='Get all posts for user'
    )
    def get(self, request, username=None):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=user)
        posts = posts.select_related('user').prefetch_related('tags', 'tagged_users')
        serializer = PostWithoutUserSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class LikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses={200: None},
        tags=['Post Like'],
        description='Like post'
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        Like.objects.get_or_create(user=request.user, post=post)
        return Response(status=200)

    @extend_schema(
        responses={200: None},
        tags=['Post Like'],
        description='Unlike post'
    )
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response(status=204)


class SavePostAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses={200: None},
        tags=['Post Save'],
        description='Save post'
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        SavedPost.objects.get_or_create(user=request.user, post=post)
        return Response(status=200)

    @extend_schema(
        responses={200: None},
        tags=['Post Save'],
        description='Unsave post'
    )
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        SavedPost.objects.filter(user=request.user, post=post).delete()
        return Response(status=204)


class SavedPostAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: PostSerializer(many=True)},
        tags=['Post'],
        description='Get saved posts'
    )
    def get(self, request):
        posts = Post.objects.filter(saved__user=request.user)
        posts = posts.select_related('user').prefetch_related('tags', 'tagged_users')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class DiscoverPostAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: PostSerializer(many=True)},
        tags=['Post'],
        description='Get discover posts'
    )
    def get(self, request):
        user = request.user
        discover_posts = Post.objects.filter(tags__in=user.interests.all())
        discover_posts = discover_posts.select_related('user').prefetch_related('tags', 'tagged_users')
        serializer = PostSerializer(discover_posts, many=True, context={'request': request})
        return Response(serializer.data)


class TagListAPIView(APIView):
    serialize_class = TagSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: serialize_class(many=True)},
        tags=['Tag'],
        description='Get all tags'
    )
    def get(self, request):
        tags = Tag.objects.all()
        serializer = self.serialize_class(tags, many=True, context={'request': request})
        return Response(serializer.data)
