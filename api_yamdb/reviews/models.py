from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from pytz import timezone


# SCORE = (
#     ('1', '1'),
#     ('2', '2'),
#     ('3', '3'),
#     ('4', '4'),
#     ('5', '5'),
#     ('6', '6'),
#     ('7', '7'),
#     ('8', '8'),
#     ('9', '9'),
#     ('10', '10'),
# )


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

    USERNAME_FIELD = 'email' # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать для входа в систему. В данном случае мы хотим использовать почту.
    REQUIRED_FIELDS = ['username'] #обязательное поле


    @property # декоратор @property возвращает атрибут свойства, позволяет обращаться к методам is_moderator() и т.п , как к свойствам в методе has_permission, has object_permissio
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


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=256
    )
    slug = models.SlugField(
        max_length=50,
        unique=True)

    def __str__(self):
        self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256
    )
    slug = models.SlugField(
        max_length=50,
        unique=True)

    def __str__(self):
        self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    # валидация year: в модели или сериализаторе
    rating = models.IntegerField(
        verbose_name='Рейтинг на основе отзывов',
        null=True,
        blank=True,
        default=None
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=250,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    def validate_year(self, value):
        if value > timezone.now().year:
            raise ValidationError(
                ('Проверьте год выхода произведения!')
            )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр(жанры)',
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} относится к жанру(жанрам): {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(verbose_name='Рейтинг',)
    pub_date = models.DateTimeField(verbose_name='Дата публикации отзыва',
                                    auto_now_add=True)

    def validators_score(self, value):
        if value < 1 and value > 10:
            raise ValidationError(
                ('Рейтинг может быть от 1 до 10')
            )
    
    class Meta:
        unique_together = ('title', 'author')
        ordering = ['pub_date']


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(verbose_name='Дата публикации отзыва',
                                    auto_now_add=True)

    class Meta:
        ordering = ['pub_date']
