from rest_framework import viewsets
from rest_framework.decorators import action
from .utils import get_shopping_list
from recipes.models import Recipe, Tag, Ingredient, IngredientRecipe
from users.models import User
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        queryset = IngredientRecipe.objects.filter(
            recipe__recipe_cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        response = get_shopping_list(queryset)
        return response

    def perform_create(self, serializer):
        print('perform create')
        serializer.is_valid()
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer