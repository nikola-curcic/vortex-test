# Generated by Django 2.2.24 on 2022-05-14 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_recipe_num_of_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='total_rating',
            field=models.IntegerField(default=0),
        ),
    ]