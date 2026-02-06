from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import BookViewSet, GenreViewSet

router = DefaultRouter()

router.register("books", BookViewSet)
router.register("genres", GenreViewSet)

urlpatterns = [path("", include(router.urls))]
