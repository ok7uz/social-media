import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    class Meta:
        db_table = 'users'
        ordering = ('first_name',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def followers_count(self):
        return Follow.objects.filter(following=self).count()

    @property
    def following_count(self):
        return Follow.objects.filter(follower=self).count()

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follows'
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow')
        ]
        verbose_name = 'follow'
        verbose_name_plural = 'follows'

    def save(self, *args, **kwargs):
        if self.follower != self.following:
            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.follower} follows {self.following}'
