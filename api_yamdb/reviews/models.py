from django.contrib.auth.models import AbstractUser
from django.db import models

SCORE = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)


class Title(models.Model):
    pass


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


class Review(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.CharField(max_length=1, choices = SCORE)
    pub_date = models.DateTimeField('Дата публикации отзыва', auto_now_add=True)


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата публикации комментария', auto_now_add=True)

