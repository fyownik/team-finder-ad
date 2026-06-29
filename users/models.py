from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=150, verbose_name='Имя')
    surname = models.CharField(max_length=150, verbose_name='Фамилия')

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    about = models.TextField(blank=True, verbose_name='О себе')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Телефон')
    github_url = models.URLField(blank=True, verbose_name='GitHub')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def save(self, *args, **kwargs):
        # Keep Django's built-in name fields in sync for admin/auth compatibility.
        self.first_name = self.name
        self.last_name = self.surname
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname}'
