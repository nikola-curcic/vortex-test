from django.db import models

# Create your models here.

class Ingredient(models.Model):
    """Ingredient model"""
    name = models.CharField(max_length=255)