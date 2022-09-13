from django.db import models


class User():
    pass


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


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=50
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50
    )


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient',
        on_delete=models.CASCADE
    )


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
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=100
    )
    image = models.ImageField(

    )
