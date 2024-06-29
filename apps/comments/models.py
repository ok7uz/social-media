from django.db import models

from apps.accounts.models import User
from apps.posts.models import Post
from apps.posts.utils import generate_id_for


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ('-created_at',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id_for(Comment)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'@{self.user.username}: {self.content}'
