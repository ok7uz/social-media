
from django.db import models

from apps.accounts.models import User


class PriceType(models.TextChoices):
    WEEK = 'week', 'Week'
    MONTH = 'month', 'Month'
    FREE = 'free', 'Free'


class ContentPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=256)
    price = models.PositiveIntegerField(null=True)
    price_type = models.CharField(max_length=10, choices=PriceType, default=PriceType.FREE)
    trial_days = models.PositiveIntegerField(null=True)
    trial_discount_percent = models.PositiveIntegerField(null=True)
    banner = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'content_plan'
        verbose_name = 'content plan'
        verbose_name_plural = 'content plans'
        ordering = ('created_at',)

    def __str__(self):
        return self.name
