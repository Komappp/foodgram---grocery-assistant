from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet,
                    ShoppingCartFavoriteRecipeAPIView, TagViewSet)

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('users/', include('users.urls')),
    path('', include('djoser.urls')),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartFavoriteRecipeAPIView.as_view()),
    path('recipes/<int:recipe_id>/favorite/',
         ShoppingCartFavoriteRecipeAPIView.as_view()),
]
