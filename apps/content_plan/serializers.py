from rest_framework import serializers

from apps.content_plan.models import ContentPlan
from apps.content.utils import TimestampField


class ContentPlanSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    created_at = TimestampField(read_only=True)

    class Meta:
        model = ContentPlan
        fields = (
            'id', 'name', 'price', 'price_type', 'banner', 'is_active',
            'description', 'trial_days', 'trial_discount_percent', 'created_at'
        )

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
