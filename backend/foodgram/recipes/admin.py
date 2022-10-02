from django.contrib import admin

from .models import (FavoritedRecipe, Recipe, Ingredient,
                     IngredientRecipe, Tag, ShoppingCart)


class Admin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class RecipeAdmin(Admin):
    list_display = ('name', 'author', 'added_to_favorited')
    list_filter = ('name', 'author', 'tags')

    def added_to_favorited(self, object):
        result = object.favorited.count()
        return result


class IngredientsAdmin(Admin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ['name', ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, Admin)
admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(IngredientRecipe, Admin)
admin.site.register(FavoritedRecipe, Admin)
admin.site.register(ShoppingCart, Admin)
