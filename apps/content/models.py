from django.db import models

from apps.accounts.models import BaseModel, User


class Tag(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    
    start_id = 10 ** 6 + 1

    class Meta:
        db_table = 'post_tags'
        ordering = ('name',)
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', db_index=True)
    caption = models.CharField(max_length=255)
    media = models.FileField(upload_to='posts/')
    tags = models.ManyToManyField(Tag, related_name='posts', db_index=True)
    tagged_users = models.ManyToManyField(User, related_name='tagged_posts', db_index=True)

    class Meta:
        db_table = 'posts'
        ordering = ('-created_at',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    @property
    def like_count(self) -> int:
        return Like.objects.filter(post=self).count()

    @property
    def comment_count(self) -> int:
        return self.comments.count()
    
    def add_tags(self, tags: list[str]) -> None:
        self.tags.clear()
        for tag in tags:
            tag_instance, _ = Tag.objects.get_or_create(name=tag)
            self.tags.add(tag_instance)

    def __str__(self):
        return self.caption


class SavedPost(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved', db_index=True)

    class Meta:
        db_table = 'post_saved'
        verbose_name = 'saved post'
        verbose_name_plural = 'saved posts'

    def __str__(self):
        return f'{self.user} saved {self.post}'


class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', db_index=True)

    class Meta:
        db_table = 'post_likes'
        verbose_name = 'like'
        verbose_name_plural = 'likes'

    def __str__(self):
        return f'{self.user} likes {self.post}'
