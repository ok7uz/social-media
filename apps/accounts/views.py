from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_spectacular.utils import extend_schema

from apps.accounts.serializers import *


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @extend_schema(
        request=serializer_class,
        responses={200: serializer_class},
        tags=['Auth'],
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
        tags=['Auth'],
        description='Register new user'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsernameCheckAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UsernameCheckSerializer

    @extend_schema(
        request=serializer_class,
        responses={200: serializer_class},
        tags=['Auth'],
        description='Check username availability'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordCheckAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordCheckSerializer

    @extend_schema(
        request=serializer_class,
        responses={200: serializer_class},
        tags=['Auth'],
        description='Check password validity'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: None},
        tags=['Auth'],
        description='Change user password'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password successfully updated."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: UserSerializer},
        tags=['Profile'],
        description='Get profile info'
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        tags=['Profile'],
        description='Update profile info'
    )
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={204: None},
        tags=['Profile'],
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
        tags=['User'],
        description='Get profile info'
    )
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class FollowAPIView(APIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses={200: None},
        tags=['Follow'],
        description='Follow user'
    )
    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        data = {
            'follower': request.user.id,
            'following': user.id
        }
        serializer = FollowSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'detail': 'Successfully followed'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFollowersAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: UserListSerializer(many=True)},
        tags=['Follow'],
        description='Get followers'
    )
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        followers = User.objects.filter(following__following=user)
        serializer = UserListSerializer(followers, many=True, context={'request': request})
        return Response(serializer.data)


class UserFollowingAPIView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: UserListSerializer(many=True)},
        tags=['Follow'],
        description='Get following'
    )
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        following = User.objects.filter(followers__follower=user)
        serializer = UserListSerializer(following, many=True, context={'request': request})
        return Response(serializer.data)
