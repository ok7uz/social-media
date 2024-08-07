from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice

from apps.accounts.models import User
from config.utils import CustomAutoField


class Notification(models.Model):

    class Types(models.TextChoices):
        FOLLOW = 'follow', 'Follow'
        CONTENT = 'content', 'Content'

    id = CustomAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    body = models.TextField()
    type = models.CharField(max_length=10, choices=Types)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ('-created_at',)

    def __str__(self):
        return f'@{self.user.username}: {self.message}'
    

class FCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fcm_tokens'
        verbose_name = 'fcm token'
        verbose_name_plural = 'fcm tokens'
        ordering = ('-created_at',)


@receiver(post_save, sender=Notification)
def notify_user(sender, instance, created, **kwargs):
    if created:
        try:
            devices = FCMDevice.objects.filter(user=instance.user)
            devices.send_message(title=instance.title, body=instance.message, data={'type': instance.type})
        except Exception as e:
            print({'error': e})
