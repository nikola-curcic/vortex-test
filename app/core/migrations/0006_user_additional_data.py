# Generated by Django 2.2.24 on 2022-05-18 11:40

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_recipe_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='additional_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
