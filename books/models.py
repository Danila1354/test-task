from django.db import models
from django.db.models import Avg, Count
from django.utils import timezone
from django.core.validators import MinValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(
        upload_to="authors/photos/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Book(models.Model):
    STATUS_CHOICES = [
        ("available", "Доступна"),
        ("out_of_stock", "Нет в наличии"),
        ("coming_soon", "Скоро в продаже"),
    ]

    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.IntegerField(default=0)
    pages = models.IntegerField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(
        upload_to="books/covers/",
        blank=True,
        null=True
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available", db_index=True
    )
    authors = models.ManyToManyField(
        "Author",
        related_name="books",
    )
    genres = models.ManyToManyField(Genre, related_name="books", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.published_date and self.published_date > timezone.now().date():
            self.status = "coming_soon"
        elif self.stock_quantity > 0:
            self.status = "available"
        else:
            self.status = "out_of_stock"

        super().save(*args, **kwargs)

    @property
    def is_available(self):
        return self.status == "available" and self.stock_quantity > 0

    def update_rating(self):
        stats = self.reviews.aggregate(avg_rating=Avg("rating"), total=Count("id"))

        self.rating = round(stats["avg_rating"] or 0, 2)
        self.total_reviews = stats["total"]
        self.save(update_fields=["rating", "total_reviews"])
