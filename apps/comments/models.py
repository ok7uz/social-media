from django.db import models

from apps.accounts.models import BaseModel, User
from apps.posts.models import Post


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    class Meta:
        db_table = 'comments'
        ordering = ('-created_at',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return f'@{self.user.username}: {self.content}'

