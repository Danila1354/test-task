import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_books_list_public(api_client, book):
    response = api_client.get("/api/v1/books/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["title"] == "Гарри Поттер и Орден Феникса"


def test_books_create_forbidden_for_user(api_client, user):
    api_client.force_authenticate(user=user)

    response = api_client.post(
        "/api/v1/books/",
        {"title": "New book", "price": 500, "pages": 200, "stock_quantity": 3},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_books_create_allowed_for_admin(api_client, admin, author, genre):
    api_client.force_authenticate(user=admin)

    response = api_client.post(
        "/api/v1/books/",
        {
            "title": "Admin book",
            "price": 800,
            "pages": 300,
            "stock_quantity": 10,
            "authors": [author.id],
            "genres": [genre.id],
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Admin book"


def test_book_serializer_returns_short_authors(api_client, book):
    response = api_client.get(f"/api/v1/books/{book.id}/")

    authors = response.data["authors"]
    assert isinstance(authors, list)
    assert "id" in authors[0]
    assert "name" in authors[0]


def test_books_create_invalid_data(api_client, admin, author, genre):
    api_client.force_authenticate(user=admin)

    response = api_client.post(
        "/api/v1/books/",
        {
            "price": 500,
            "pages": 100,
            "stock_quantity": 2,
            "authors": [author.id],
            "genres": [genre.id],
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.data

    response = api_client.post(
        "/api/v1/books/",
        {
            "title": "Invalid book",
            "price": -100,
            "pages": 100,
            "stock_quantity": 2,
            "authors": [author.id],
            "genres": [genre.id],
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "price" in response.data
