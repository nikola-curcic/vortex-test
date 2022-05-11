from rest_framework import serializers
from core.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()