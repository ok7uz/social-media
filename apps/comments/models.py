from django.db import models

from apps.accounts.models import User
from apps.content.models import Post


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', db_index=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', db_index=True)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'comments'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ('-created_at',)

    def __str__(self):
        return f'@{self.user.username}: {self.content}'
