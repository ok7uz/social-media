from datetime import date
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    interests = models.ManyToManyField('content.Tag', related_name='users', blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'users'
        ordering = ('-created_at',)
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = [
            models.Index(fields=['username']),
        ]

    @property
    def post_count(self) -> int:
        return self.posts.count()

    @property
    def follower_count(self) -> int:
        return Follow.objects.filter(following=self).count()

    @property
    def following_count(self) -> int:
        return Follow.objects.filter(follower=self).count()

    @property
    def age(self) -> Optional[int]:
        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year
            if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
                age -= 1
            return age
        return None

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, db_index=True)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, db_index=True)

    class Meta:
        db_table = 'user_follows'
        unique_together = ('follower', 'following')
        verbose_name = 'follow'
        verbose_name_plural = 'follows'

    def __str__(self):
        return f'{self.follower} follows {self.following}'
