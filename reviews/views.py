from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from books.models import Book
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .permissions import IsOwnerOrReadOnly
from .serializers import ReviewSerializer


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
