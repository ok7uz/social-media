import uuid

from django.db import models

from apps.accounts.models import User
from apps.posts.utils import generate_id_for


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'post_tags'
        ordering = ('name',)
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'
        ordering = ('-created_at',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    @property
    def likes_count(self) -> int:
        return Like.objects.filter(post=self).count()

    @property
    def comments_count(self) -> int:
        return self.comments.count()
    
    def add_tags(self, tags: list[str]) -> None:
        self.tags.clear()
        for tag in tags:
            tag_instance, _ = Tag.objects.get_or_create(name=tag)
            self.tags.add(tag_instance)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id_for(Post)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SavedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')

    class Meta:
        db_table = 'post_saved'
        verbose_name = 'saved post'
        verbose_name_plural = 'saved posts'

    def __str__(self):
        return f'{self.user} saved {self.post}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        db_table = 'post_likes'
        verbose_name = 'like'
        verbose_name_plural = 'likes'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id_for(Like)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} likes {self.post}'
