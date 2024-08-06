from django.db import models

from apps.accounts.models import User
from config.utils import CustomAutoField


class Chat(models.Model):
    id = CustomAutoField(primary_key=True, editable=False, start_value=10 ** 6 + 1)
    name = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='chats/images/', null=True)
    owner = models.ForeignKey(User, related_name='owned_chats', on_delete=models.SET_NULL, null=True, db_index=True)
    participants = models.ManyToManyField(User, related_name='chats')
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'chats'
        verbose_name = 'chat'
        verbose_name_plural = 'chats'
        ordering = ('-created_at',)


class MediaType(models.TextChoices):
    IMAGE = 'image', 'Image'
    VIDEO = 'video', 'Video'
    FILE = 'file', 'File'
    VOICE = 'voice', 'Voice'


class Message(models.Model):
    id = CustomAutoField(primary_key=True, editable=False)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, db_index=True)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.SET_NULL, null=True, db_index=True)
    content = models.TextField(null=True)
    media = models.FileField(upload_to='messages/media/', null=True)
    media_type = models.CharField(max_length=10, choices=MediaType, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'messages'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('created_at',)
