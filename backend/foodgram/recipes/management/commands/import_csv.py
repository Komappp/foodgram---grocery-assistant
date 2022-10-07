from csv import DictReader
from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Loads data from ingredients.csv"

    def handle(self, *args, **options):

        if Ingredient.objects.exists():
            print('данные загружены ....выход')
            return

        print('Загрузка ингредиентов в базу данных')

        for row in DictReader(open('./ingredients.csv')):
            ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row['measure']
            )
            ingredient.save()
