
from django.db import models

from apps.accounts.models import BaseModel, User


class PriceType(models.TextChoices):
    WEEK = 'week', 'Week'
    MONTH = 'month', 'Month'
    FREE = 'free', 'Free'


class Status(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class ContentPlan(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(null=True)
    price_type = models.CharField(max_length=10, choices=PriceType, default=PriceType.FREE)
    trial_days = models.PositiveIntegerField(null=True, blank=True)
    trial_discount_percent = models.PositiveIntegerField(null=True, blank=True)
    banner = models.ImageField(upload_to='banners/')
    status = models.CharField(max_length=10, choices=Status, default=Status.ACTIVE)
    description = models.TextField(max_length=250)

    class Meta:
        db_table = 'content_plan'
        verbose_name = 'content plan'
        verbose_name_plural = 'content plans'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

