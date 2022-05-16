from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        exclude = ('num_of_ratings', 'total_rating', 'user')
        read_only_fields = ('average_rating', 'num_of_ratings', 'total_rating')


def valid_rating(value):
    if value < 1 or value > 5:
        raise serializers.ValidationError('Serializer not correct')


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(validators=[valid_rating])



