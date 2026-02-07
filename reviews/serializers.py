from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "rating",
            "comment",
            "user",
            "username",
            "book",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "book", "created_at", "updated_at"]
