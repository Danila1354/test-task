from rest_framework import viewsets
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

from .models import Book, Genre, Author
from .serializers import (
    BookCreateUpdateSerializer,
    BookSerializer,
    GenreSerializer,
    AuthorSerializer,
)
from .permissions import IsAdminOrReadOnly

@extend_schema_view(
    list=extend_schema(
        summary="Список книг",
        description="Получить список всех книг (доступно всем)",
        responses={200: BookSerializer},
    ),
    retrieve=extend_schema(
        summary="Детальная информация о книге",
        description="Получить одну книгу по ID",
        responses={200: BookSerializer},
    ),
    create=extend_schema(
        summary="Создать книгу",
        description="Создание книги (только для администратора)",
        request=BookCreateUpdateSerializer,
        responses={
            201: BookSerializer,
            403: OpenApiResponse(description="Недостаточно прав"),
        },
    ),
    update=extend_schema(
        summary="Обновить книгу",
        description="Полное обновление книги (только администратор)",
        request=BookCreateUpdateSerializer,
    ),
    partial_update=extend_schema(
        summary="Частично обновить книгу",
        description="Частичное обновление книги (только администратор)",
        request=BookCreateUpdateSerializer,
    ),
    destroy=extend_schema(
        summary="Удалить книгу",
        description="Удаление книги (только администратор)",
        responses={204: OpenApiResponse(description="Удалено")},
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().prefetch_related("authors", "genres")
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return BookCreateUpdateSerializer
        return BookSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Список жанров",
        description="Получить список жанров",
    ),
    retrieve=extend_schema(
        summary="Детальный жанр",
    ),
    create=extend_schema(
        summary="Создать жанр",
        description="Создание жанра (только администратор)",
    ),
    update=extend_schema(summary="Обновить жанр"),
    partial_update=extend_schema(summary="Частично обновить жанр"),
    destroy=extend_schema(summary="Удалить жанр"),
)
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    list=extend_schema(
        summary="Список авторов",
        description="Получить список авторов",
    ),
    retrieve=extend_schema(
        summary="Детальный автор",
    ),
    create=extend_schema(
        summary="Создать автора",
        description="Создание автора (только администратор)",
    ),
    update=extend_schema(summary="Обновить автора"),
    partial_update=extend_schema(summary="Частично обновить автора"),
    destroy=extend_schema(summary="Удалить автора"),
)
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
