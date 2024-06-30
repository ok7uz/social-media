from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from apps.posts.models import Tag

from .models import User
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, FollowSerializer, UserListSerializer
from drf_spectacular.utils import extend_schema


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @extend_schema(
        request=serializer_class,
        responses={200: serializer_class},
        tags=['auth'],
        description='Login user'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @extend_schema(
        request=serializer_class,
        responses={201: serializer_class},
        tags=['auth'],
        description='Register new user'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_serializer = UserSerializer(serializer.instance, context={'request': request})
            return Response(user_serializer.data, status=201)

        return Response(serializer.errors, status=400)


class ProfileAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: UserSerializer},
        tags=['profile'],
        description='Get profile info'
    )
    def get(self, request, username=None):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        tags=['profile'],
        description='Update profile info'
    )
    def put(self, request, username=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={204: None},
        tags=['profile'],
        description='Delete profile'
    )
    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: UserSerializer},
        tags=['profile'],
        description='Get profile info'
    )
    def get(self, request, username=None):
        user = get_object_or_404(User, username=username) if username else request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class FollowAPIView(APIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=FollowSerializer,
        responses={200: serializer_class},
        tags=['follow'],
        description='Follow user'
    )
    def post(self, request, username=None):
        user = get_object_or_404(User, username=username)
        data = {
            'follower': request.user.id,
            'following': user.id
        }
        serializer = FollowSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        user_serializer = UserSerializer(user, context={'request': request})
        return Response(user_serializer.data)


class UserFollowersAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: UserListSerializer(many=True)},
        tags=['follow'],
        description='Get followers'
    )
    def get(self, request, username=None):
        user = get_object_or_404(User, username=username)
        followers = User.objects.filter(following__following=user)
        serializer = UserListSerializer(followers, many=True, context={'request': request})
        return Response(serializer.data)


class UserFollowingAPIView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: UserListSerializer(many=True)},
        tags=['follow'],
        description='Get following'
    )
    def get(self, request, username=None):
        user = get_object_or_404(User, username=username)
        following = User.objects.filter(followers__follower=user)
        serializer = UserListSerializer(following, many=True, context={'request': request})
        return Response(serializer.data)

