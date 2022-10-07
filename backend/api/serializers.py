import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from recipes.models import (FavoritedRecipe, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag)
from rest_framework import serializers
from users.models import Following

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if request.user.id is None:
            return False
        return Following.objects.filter(follow=obj,
                                        follower=request.user).exists()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='pic.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(source='recipe_ingredient',
                                             many=True, required=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context['request']
        if request.user.id is None:
            return False
        return FavoritedRecipe.objects.filter(recipe=obj,
                                              user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        if request.user.id is None:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'image',
                  'name', 'text', 'cooking_time')

    def create_ingredient_recipe(self, ingredients_data, recipe):
        model_instances = [IngredientRecipe(
            ingredient_id=ingredient['id'],
            recipe=recipe,
            amount=ingredient['amount']
        ) for ingredient in ingredients_data]
        IngredientRecipe.objects.bulk_create(model_instances)

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            image=image, **validated_data,
            author=self.context.get('request').user
        )
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredient_recipe(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientRecipe.objects.filter(recipe=instance).all().delete()
        self.create_ingredient_recipe(
            validated_data.get('ingredients'), instance
        )
        instance.save()
        return instance

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError({
                    'ingredients': ('Число игредиентов должно быть больше 0')
                })
        data['ingredients'] = ingredients
        return data


class RecipeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def validate(self, data):
        user_id = data['user']
        recipe_id = data['recipe']
        if ShoppingCart.objects.filter(
            user_id=user_id, recipe_id=recipe_id
        ).exists():
            raise serializers.ValidationError(
                "Рецепт уже добавлен в корзину"
            )
        return data


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoritedRecipe
        fields = '__all__'

    def validate(self, data):
        user_id = data['user']
        recipe_id = data['recipe']
        if FavoritedRecipe.objects.filter(
            user_id=user_id, recipe_id=recipe_id
        ).exists():
            raise serializers.ValidationError(
                "Рецепт уже добавлен в избранное"
            )
        return data
