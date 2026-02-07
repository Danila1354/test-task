import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from books.models import Book, Author, Genre
from reviews.models import Review

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="user",
        password="123456"
    )


@pytest.fixture
def admin(db):
    return User.objects.create_superuser(
        username="admin1",
        password="123456"
    )


@pytest.fixture
def genre(db):
    return Genre.objects.create(name="Фантастика")


@pytest.fixture
def author(db):
    return Author.objects.create(
        name="Дж. К. Роулинг",
        country="Великобритания"
    )

@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="other", password="pass")

@pytest.fixture
def book(db, author, genre):
    book = Book.objects.create(
        title="Гарри Поттер и Орден Феникса",
        price=1000,
        stock_quantity=5,
        pages=500
    )
    book.authors.add(author)
    book.genres.add(genre)
    return book

@pytest.fixture
def review(db, other_user, book):
    return Review.objects.create(
        user=other_user,
        book=book,
        rating=5,
        comment="Отличная книга"
    )