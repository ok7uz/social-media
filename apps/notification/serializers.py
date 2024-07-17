from rest_framework import serializers

from apps.notification.models import Notification
from config.utils import TimestampField


class NotificationSerializer(serializers.ModelSerializer):
    created_at = TimestampField(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'message', 'created_at')
