from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('average_rating',)

