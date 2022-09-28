from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from .utils import get_shopping_list
from recipes.models import Recipe, Tag, Ingredient, IngredientRecipe
from users.models import User
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeWriteSerializer, ShoppingCartSerializer,
                          TagSerializer, ShoppingCart)
from rest_framework import generics, status
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeWriteSerializer
        return RecipeSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = RecipeWriteSerializer
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     serializer = RecipeSerializer
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        queryset = IngredientRecipe.objects.filter(
            recipe__recipe_cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        response = get_shopping_list(queryset)
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class ShoppingCartAPIView(APIView):
    def post(self, request):
        serializer = ShoppingCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pass
