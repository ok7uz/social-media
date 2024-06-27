import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, validators=[username_validator], verbose_name='username')
    first_name = models.CharField(max_length=150, verbose_name='first name')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='last name')
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    class Meta:
        db_table = 'users'
        ordering = ('first_name',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
