from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import GetPostDeleteViewSet
from .permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReadOnlyTitleSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitleSerializer, TokenSerializer, UserEditSerializer,
                          UserSerializer)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    """Отправка письма с кодом подтверждения (confirmation_code) на адрес email"""
    pass


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Получение JWT-токена в обмен на username и confirmation code."""
    pass


class UserViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование пользовательских данных"""
    pass


class CategoryViewSet(GetPostDeleteViewSet):
    """Просмотр и редактирование категорий произведений"""
    lookup_field = "slug"
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenreViewSet(GetPostDeleteViewSet):
    """Просмотр и редактирование жанров произведений"""
    lookup_field = "slug"
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class TitleViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование  произведений"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование отзывов на  произведения"""
    pass


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование комментариев к отзывам"""
    pass
