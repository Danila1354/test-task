from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from books.models import Book


from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs["book_pk"]).select_related(
            "user", "book"
        )

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs["book_pk"])
        user = self.request.user

        if Review.objects.filter(book=book, user=user).exists():
            raise ValidationError({"detail": "Вы уже оставили отзыв на эту книгу."})

        serializer.save(book=book, user=user)
