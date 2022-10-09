from django.db import models
from django.db.models import UniqueConstraint
from django.http import HttpResponse
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=30
    )
    color = models.CharField(
        verbose_name='Цвет в HEX формате',
        max_length=7
    )
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=100,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50
    )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes'
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиенты',
        through='IngredientRecipe'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=100,
        db_index=True
    )
    image = models.ImageField(
        upload_to='pics/',
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']

    @staticmethod
    def get_shopping_list(queryset):
        """Передает ингредиенты txt файлом в HTTP-response"""

        string_len = 70
        shopping_list = ''
        ingredients = {}
        for i in queryset:
            key, value = i[0] + ',' + i[1], i[2]
            if key in ingredients:
                ingredients[key] += value
                continue
            ingredients[key] = value
        for key, value in ingredients.items():
            ingr, unit = key.split(',')
            space_count = (string_len - len(ingr + str(i[2]))) * ' '
            shopping_list += f'{ingr} {space_count} {value} {unit}\n'
        print(shopping_list)
        response = HttpResponse(shopping_list, content_type='text/txt')
        string = 'attachment;filename=shopping_list.txt'
        response['Content-Disposition'] = string
        return response

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe_ingredient',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredient',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()

    class Meta:
        UniqueConstraint(
            fields=['ingredient', 'recipe'], name='unique_ingredient'
        )

    def __str__(self):
        return (
            f'{self.amount} {self.ingredient.measurement_unit} '
            f'{self.ingredient} в рецепте {self.recipe}'
        )


class FavoritedRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited'
    )

    class Meta:
        UniqueConstraint(fields=['user', 'recipe'], name='unique_favorited')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_cart'
    )

    class Meta:
        UniqueConstraint(fields=['user', 'recipe'], name='unique_favorited')
