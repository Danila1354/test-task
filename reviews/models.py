from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, max_length=2048)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="reviews"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
        unique_together = [["user", "book"]]

    def __str__(self):
        return f"Отзыв от {self.user.email} на '{self.book.title}' - {self.rating}/5"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_rating()

    def delete(self, *args, **kwargs):
        book = self.book
        super().delete(*args, **kwargs)
        book.update_rating()
