import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_genre_list_public(api_client, genre):
    """Любой пользователь может получить список жанров."""
    response = api_client.get("/api/v1/genres/")
    assert response.status_code == status.HTTP_200_OK


def test_genre_create_forbidden_for_user(api_client, user):
    """Обычный пользователь не может создавать жанры."""
    api_client.force_authenticate(user=user)

    response = api_client.post("/api/v1/genres/", {
        "name": "Sci-Fi"
    })

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_genre_create_allowed_for_admin(api_client, admin):
    """Администратор может создать жанр."""
    api_client.force_authenticate(user=admin)

    response = api_client.post("/api/v1/genres/", {
        "name": "Sci-Fi"
    })

    assert response.status_code == status.HTTP_201_CREATED

def test_genre_name_unique(api_client, admin, genre):
    """Нельзя создать жанр с уже существующим именем."""
    api_client.force_authenticate(user=admin)

    response = api_client.post("/api/v1/genres/", {
        "name": genre.name
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data