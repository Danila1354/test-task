from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from books.models import Book
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)

from .models import Review
from .permissions import IsOwnerOrReadOnly
from .serializers import ReviewSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Список отзывов книги",
        description=(
            "Получить список отзывов для конкретной книги.\n\n"
            "Доступно всем пользователям."
        ),
        parameters=[
            OpenApiParameter(
                name="book_pk",
                description="ID книги",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={200: ReviewSerializer},
    ),
    retrieve=extend_schema(
        summary="Детальный отзыв",
        description="Получить один отзыв по ID (в рамках книги).",
        parameters=[
            OpenApiParameter(
                name="book_pk",
                description="ID книги",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={200: ReviewSerializer},
    ),
    create=extend_schema(
        summary="Создать отзыв",
        description=(
            "Создать отзыв на книгу.\n\n"
            "Требуется аутентификация.\n"
            "Один пользователь может оставить только один отзыв на книгу."
        ),
        request=ReviewSerializer,
        responses={
            201: ReviewSerializer,
            400: OpenApiResponse(description="Отзыв уже существует или некорректные данные"),
            401: OpenApiResponse(description="Требуется аутентификация"),
        },
    ),
    update=extend_schema(
        summary="Полностью обновить отзыв",
        description=(
            "Полное обновление отзыва.\n\n"
            "⚠ Требуется передать все поля отзыва.\n"
            "Доступно только владельцу отзыва."
        ),
        request=ReviewSerializer,
        responses={
            200: ReviewSerializer,
            400: OpenApiResponse(description="Некорректные данные"),
            403: OpenApiResponse(description="Недостаточно прав"),
        },
    ),
    partial_update=extend_schema(
        summary="Изменить отзыв",
        description="Частичное обновление отзыва (только владелец отзыва).",
        responses={
            200: ReviewSerializer,
            403: OpenApiResponse(description="Недостаточно прав"),
        },
    ),
    destroy=extend_schema(
        summary="Удалить отзыв",
        description="Удалить отзыв (только владелец отзыва).",
        responses={
            204: OpenApiResponse(description="Отзыв удалён"),
            403: OpenApiResponse(description="Недостаточно прав"),
        },
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs["book_pk"]).select_related(
            "user", "book"
        )

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs["book_pk"])
        user = self.request.user

        if Review.objects.filter(book=book, user=user).exists():
            raise ValidationError({"detail": "Вы уже оставили отзыв на эту книгу."})

        serializer.save(book=book, user=user)
