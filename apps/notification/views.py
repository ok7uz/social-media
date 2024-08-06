from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.openapi import OpenApiResponse
from drf_spectacular.utils import extend_schema

from apps.notification.serializers import FCMTokenSerializer, NotificationSerializer


class NotificationView(APIView):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated, )

    @extend_schema(
        responses={200: NotificationSerializer(many=True)},
        tags=['Notification'],
        description='Get all notifications'
    )
    def get(self, request):
        notifications = request.user.notifications.all()
        serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaveFCMTokenView(APIView):
    serializer_class = FCMTokenSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=FCMTokenSerializer,
        responses={201: OpenApiResponse(description='FCM token saved.')},
        tags=['Notification'],
        description='Save FCM token'
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"message": "FCM token saved."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
