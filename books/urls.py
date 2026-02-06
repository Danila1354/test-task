from rest_framework_nested import routers
from django.urls import path, include
from .views import BookViewSet, GenreViewSet, AuthorViewSet
from reviews.views import ReviewViewSet

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("genres", GenreViewSet)
router.register("authors", AuthorViewSet)

books_router = routers.NestedDefaultRouter(router, "books", lookup="book")
books_router.register("reviews", ReviewViewSet, basename="book-reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(books_router.urls)),
]