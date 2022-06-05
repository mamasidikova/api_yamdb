from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию и десериализацию объектов User. """
    pass


class UserEditSerializer(serializers.ModelSerializer):
    pass


class RegistrationSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию запросов регистрации объектов User. """
    pass


class TokenSerializer(serializers.Serializer):
    """ Осуществляет сериализацию генерируемых токенов объектов User. """
    pass


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию и десериализацию объектов Genre. """
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию и десериализацию объектов Title. """
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию и десериализацию объектов Title
    при get-запросах.
    """
    rating = serializers.SerializerMethodField(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True)
    category = CategorySerializer(
        read_only=True,
        many=False
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        all_reviews = obj.reviews.all()
        avg_rating = all_reviews.aggregate(Avg('score')).get('score__avg')
        if avg_rating is not None:
            return avg_rating
        return None


class ReviewSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию и десериализацию объектов Review. """
    pass


class CommentSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию и десериализацию объектов Comment. """
    pass

