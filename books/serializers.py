from rest_framework import serializers

from .models import Book, Author



class AuthorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name")


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorShortSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = [
            "title",
            "description",
            "price",
            "stock_quantity",
            "pages",
            "published_date",
            "cover_image",
            "rating",
            "total_reviews",
            "status",
            "authors",
            "genres",
            "created_at",
            "updated_at",
        ]

class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "title",
            "description",
            "price",
            "stock_quantity",
            "pages",
            "published_date",
            "cover_image",
            "authors",
            "genres",
        )