# Generated by Django 2.2.24 on 2022-05-14 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_recipe_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='num_of_ratings',
            field=models.IntegerField(default=0),
        ),
    ]
