# Generated by Django 3.2.15 on 2022-10-08 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_ingredient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Название ингридиента'),
        ),
    ]
