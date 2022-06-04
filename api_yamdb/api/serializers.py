from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Осуществляет сериализацию и десериализацию объектов User. """
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), 
            message=("Username already exists")) # встроенный класс валидатор, принудительно примененяем ограничения unique=True для поля username модели
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

