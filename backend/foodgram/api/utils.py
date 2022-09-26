from django.http import HttpResponse


def get_shopping_list(queryset):
    """Передает ингредиенты txt файлом в HTTP-response"""
    STRING_LEN = 70
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
        space_count = (STRING_LEN-len(ingr+unit+str(i[2])))*' '
        shopping_list += f'{ingr} {space_count} {value} {unit}\n'
    print(shopping_list)
    response = HttpResponse(shopping_list, content_type='text/plane')
    response['Content-Disposition'] = f'attachment; filename=shopping_list.txt'
    return response
