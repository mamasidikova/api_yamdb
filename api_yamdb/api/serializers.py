from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию и десериализацию объектов User. """
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), 
            message=("Username already exists"))
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all(),
            message=("Email already exists"))
        ]
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegistrationSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию запросов регистрации объектов User. """
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is prohibited")
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    """ Осуществляет сериализацию генерируемых токенов объектов User. """
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


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
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title_id, author=user).exists():
                raise ValidationError(
                    'Вы уже оставляли отзыв на это произведение.'
                )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию и десериализацию объектов Comment. """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

