from django.http import JsonResponse
from recipes.models import Recipe
from .serializers import RecipeSerializer
from django.shortcuts import get_object_or_404


def get_recipe(request, pk):
    if request.method == 'GET':
        post = get_object_or_404(Recipe, id=pk)
        serializer = RecipeSerializer(post, many=False)
        return JsonResponse(serializer.data)
