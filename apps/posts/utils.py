from rest_framework import serializers


class TimestampField(serializers.IntegerField):

    def to_representation(self, value) -> int:
        return int(value.timestamp())
