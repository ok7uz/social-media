from django.db import models
from rest_framework import serializers


class CustomAutoField(models.IntegerField):

    def __init__(self, *args, **kwargs):
        self.start_value = kwargs.pop('start_value', 10 ** 9 + 1)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and getattr(model_instance, self.attname) is None:
            last_instance = model_instance.__class__.objects.order_by('-id').first()
            if last_instance:
                value = max(last_instance.id + 1, self.start_value)
            else:
                value = self.start_value
            setattr(model_instance, self.attname, value)
        return super().pre_save(model_instance, add)


class TimestampField(serializers.IntegerField):

    def to_representation(self, value) -> int:
        return int(value.timestamp())
