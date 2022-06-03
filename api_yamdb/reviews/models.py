from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


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
    pass


class Comment(models.Model):
    pass
