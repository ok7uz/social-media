from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User
from config.utils import CustomAutoField


class Notification(models.Model):
    id = CustomAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ('-created_at',)

    def __str__(self):
        return f'@{self.user.username}: {self.message}'


@receiver(post_save, sender=Notification)
def notify_user(sender, instance, created, **kwargs):
    if created:
        group_name = f'user_{instance.user.id}'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                'text': instance.message
            }
        )
