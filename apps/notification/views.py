from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notification.serializers import NotificationSerializer


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
