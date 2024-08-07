from rest_framework import serializers

from apps.notification.models import Notification, FCMToken
from config.utils import TimestampField


class NotificationSerializer(serializers.ModelSerializer):
    created_at = TimestampField(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'title', 'body', 'type', 'created_at')


class FCMTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = FCMToken
        fields = ['token']
