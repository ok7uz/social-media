from django.db import models

from apps.accounts.models import BaseModel, User


class Chat(BaseModel):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='chats')
    is_group = models.BooleanField(default=False)

    class Meta:
        db_table = 'chats'
        verbose_name = 'chat'
        verbose_name_plural = 'chats'
        ordering = ('-created_at',)

class Message(BaseModel):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.SET_NULL, null=True)
    content = models.TextField()

    class Meta:
        db_table = 'messages'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-created_at',)
