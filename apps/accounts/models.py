import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.utils import generate_id_for


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)

    class Meta:
        db_table = 'users'
        ordering = ('first_name',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def posts_count(self) -> int:
        return self.posts.count()

    @property
    def followers_count(self) -> int:
        return Follow.objects.filter(following=self).count()

    @property
    def following_count(self) -> int:
        return Follow.objects.filter(follower=self).count()

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id_for(User)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_follows'
        verbose_name = 'follow'
        verbose_name_plural = 'follows'

    def save(self, *args, **kwargs):
        if self.follower != self.following:
            if not self.id:
                self.id = generate_id_for(Follow)
            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.follower} follows {self.following}'


class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    tag = models.ForeignKey('posts.Tag', on_delete=models.CASCADE, related_name='interests')

    class Meta:
        db_table = 'user_interests'
        ordering = ('user', 'tag')
        verbose_name = 'interest'
        verbose_name_plural = 'interests'

    def __str__(self):
        return self.name
