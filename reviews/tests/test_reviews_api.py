import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_reviews_list_public(api_client, review, book):
    """Любой пользователь может посмотреть отзывы книги"""
    response = api_client.get(f"/api/v1/books/{book.id}/reviews/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["rating"] == review.rating


def test_create_review_authenticated(api_client, user, book):
    """Аутентифицированный пользователь может оставить отзыв"""
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/api/v1/books/{book.id}/reviews/", {
        "rating": 4,
        "comment": "Неплохая книга"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["rating"] == 4
    assert response.data["comment"] == "Неплохая книга"


def test_create_review_unauthenticated(api_client, book):
    """Неавторизованный пользователь не может оставить отзыв"""
    response = api_client.post(f"/api/v1/books/{book.id}/reviews/", {
        "rating": 5,
        "comment": "Отлично!"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_duplicate_review(api_client, other_user, review):
    """Нельзя оставить два отзыва на одну книгу от одного пользователя"""
    api_client.force_authenticate(user=other_user)
    book_id = review.book.id
    response = api_client.post(f"/api/v1/books/{book_id}/reviews/", {
        "rating": 5,
        "comment": "Повторный отзыв"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data


def test_update_review_by_owner(api_client, review):
    """Автор отзыва может его изменить"""
    api_client.force_authenticate(user=review.user)
    response = api_client.patch(f"/api/v1/books/{review.book.id}/reviews/{review.id}/", {
        "rating": 3
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.data["rating"] == 3


def test_update_review_by_other_user_forbidden(api_client, review, user):
    """Другой пользователь не может изменить чужой отзыв"""
    api_client.force_authenticate(user=user)
    response = api_client.patch(f"/api/v1/books/{review.book.id}/reviews/{review.id}/", {
        "rating": 1
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_review_by_owner(api_client, review):
    """Автор отзыва может удалить его"""
    api_client.force_authenticate(user=review.user)
    response = api_client.delete(f"/api/v1/books/{review.book.id}/reviews/{review.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_review_by_other_user_forbidden(api_client, review, user):
    """Другой пользователь не может удалить чужой отзыв"""
    api_client.force_authenticate(user=user)
    response = api_client.delete(f"/api/v1/books/{review.book.id}/reviews/{review.id}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_rating_validation(api_client, user, book):
    """Нельзя создать отзыв с рейтингом вне 1-5"""
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/api/v1/books/{book.id}/reviews/", {
        "rating": 6,
        "comment": "Слишком высокий рейтинг"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "rating" in response.data