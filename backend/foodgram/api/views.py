from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (FavoritedRecipe, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import IngredientSearchFilter, RecipeFilters
from .pagination import RecipesPagination
from .permissions import IsOwnerOrStuffOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          RecipeWriteSerializer, ShoppingCartSerializer,
                          TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',)
    filterset_class = RecipeFilters
    pagination_class = RecipesPagination
    permission_classes = [IsOwnerOrStuffOrReadOnly, ]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeWriteSerializer
        return RecipeSerializer

    @action(detail=False, url_path='download_shopping_cart',
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        queryset = IngredientRecipe.objects.filter(
            recipe__recipe_cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        response = Recipe.get_shopping_list(queryset)
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeSerializer(
            instance=serializer.instance,
            context={'request': self.request}
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsOwnerOrStuffOrReadOnly, ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('name', )
    permission_classes = [IsOwnerOrStuffOrReadOnly, ]


class ShoppingCartFavoriteRecipeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, request, data):
        if self.is_shopping(request):
            return ShoppingCartSerializer(data=data)
        else:
            return FavoriteSerializer(data=data)

    def is_shopping(self, request):
        return 'shopping' in request.path

    def post(self, request, recipe_id):
        user = request.user
        data = {
            'recipe': recipe_id,
            'user': user.id
        }
        serializer = self.get_serializer_class(request, data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            serializer_to_response = RecipeShortSerializer(
                Recipe.objects.get(id=recipe_id)
            )
            return Response(serializer_to_response.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if self.is_shopping(request):
            model = ShoppingCart
        else:
            model = FavoritedRecipe
        model.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
