from django.contrib import admin
from .models import Book, Author, Genre
from reviews.models import Review

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "birth_date")
    search_fields = ("name", "country")
    list_filter = ("country",)
    ordering = ("name",)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0 
    readonly_fields = ("user", "rating", "comment", "created_at", "updated_at")
    can_delete = True 
    show_change_link = True 


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "status",
        "stock_quantity",
        "rating",
        "total_reviews",
        "created_at",
    )
    list_filter = ("status", "genres")
    search_fields = ("title", "authors__name")
    ordering = ("-created_at",)
    filter_horizontal = ("genres", "authors")
    inlines = [ReviewInline]