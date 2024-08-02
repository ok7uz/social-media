from rest_framework import serializers

from apps.content.serializers import PostSerializer
from apps.content_plan.models import ContentPlan
from config.utils import TimestampField


class ContentPlanSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    created_at = TimestampField(read_only=True)
    subscriber_count = serializers.SerializerMethodField(read_only=True)
    length = serializers.SerializerMethodField(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = ContentPlan
        fields = (
            'id', 'name', 'price', 'price_type', 'banner', 'is_active', 'description', 'subscriber_count', 'length',
            'trial_days', 'trial_discount_percent', 'trial_description', 'created_at', 'posts'
        )

    def get_subscriber_count(self, obj) -> int:
        return obj.users.count()

    def get_length(self, obj) -> int:
        return 'Not available'

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ContentPlanListSerializer(serializers.ModelSerializer):
    created_at = TimestampField(read_only=True)

    class Meta:
        model = ContentPlan
        fields = (
            'id', 'name', 'price', 'price_type', 'banner', 'is_active', 'description', 'created_at',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    created_at = TimestampField(read_only=True)

    class Meta:
        model = ContentPlan
        fields = ('id', 'name', 'price', 'price_type', 'banner', 'is_active', 'created_at')
