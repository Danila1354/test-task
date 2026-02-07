import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_author_list_public(api_client, author):
    response = api_client.get("/api/v1/authors/")
    assert response.status_code == status.HTTP_200_OK


def test_author_create_forbidden_for_user(api_client, user):
    api_client.force_authenticate(user=user)

    response = api_client.post("/api/v1/authors/", {
        "name": "Достоевский",
        "country": "Россия"
    })

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_author_create_allowed_for_admin(api_client, admin):
    api_client.force_authenticate(user=admin)

    response = api_client.post("/api/v1/authors/", {
        "name": "Достоевский",
        "country": "Россия"
    })

    assert response.status_code == status.HTTP_201_CREATED


def test_author_create_invalid_data(api_client, admin):
    api_client.force_authenticate(user=admin)

    response = api_client.post("/api/v1/authors/", {
        "name": "",
        "country": "Россия"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
