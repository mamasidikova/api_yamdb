from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    username = models.CharField(
        verbose_name='Пользователь',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Почтовый адрес',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='Информация о пользователе',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email' # идентификатор для обращения
    REQUIRED_FIELDS = ['username'] #обязательное поле


    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    
    @property
    def is_user(self):
        return self.role == self.USER

    
    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
