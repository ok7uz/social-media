from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User


class ProfileAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={200: UserSerializer},
        tags=['Profile'],
        description='Get profile info'
    )
    def get(self, request):
        serializer = self.serializer_class(request.user, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        tags=['Profile'],
        description='Update profile info'
    )
    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True, context={'request': request})
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
        request.user.delete()
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
        serializer = self.serializer_class(user, context={'request': request})
        return Response(serializer.data)
