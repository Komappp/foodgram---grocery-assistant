from django import views
from django.urls import path, include
from .views import RecipeViewSet, IngredientViewSet, TagViewSet
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

router = SimpleRouter()
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
