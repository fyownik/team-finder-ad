from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import USER_NAME_MAX_LENGTH, USER_PHONE_MAX_LENGTH


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        verbose_name='Фамилия'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    about = models.TextField(blank=True, verbose_name='О себе')
    phone = models.CharField(
        max_length=USER_PHONE_MAX_LENGTH,
        blank=True,
        verbose_name='Телефон'
    )
    github_url = models.URLField(blank=True, verbose_name='GitHub')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def __str__(self):
        return f'{self.name} {self.surname}'
