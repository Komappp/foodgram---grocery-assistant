from tabnanny import verbose
from django.db import models
from django.forms import CharField, SlugField


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
    name = CharField(
        verbose_name='Название ингридиента',
        max_length=50
    )
    measurement_unit = CharField(
        verbose_name='Единица измерения',
        max_length=50
    )


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=100
    )
    image = models.ImageField(

    )
