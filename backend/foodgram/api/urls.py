from django.urls import path, include
from .views import RecipeViewSet, IngredientViewSet, TagViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
