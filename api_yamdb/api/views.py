from reviews.models import Category, Genre, Title
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import (IsAuthenticated,
#                                         IsAuthenticatedOrReadOnly)
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins

from .permissions import IsAdminSuperuserOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          ReadOnlyTitleSerializer)
from .filters import TitleFilter


class GetPostDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminSuperuserOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = "slug"


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminSuperuserOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [IsAdminSuperuserOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('category', 'genre', 'name', 'year',)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        # Если запрошенное действие (action) — получение списка объектов ('list')
        if self.action in ('list', 'retrieve'):
            # ...то применяем CatListSerializer
            return ReadOnlyTitleSerializer
        # А если запрошенное действие — не 'list', применяем CatSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
