from django.core import serializers
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.repository import (
                                list_recipes_db,
                                get_recipe_db,
                                list_own_recipes_db,
                                rate_recipe_db,
                                list_recipes_max_min_ingredients_db,
                                list_recipes_name_db,
                                list_recipes_text_db,
                                list_recipes_ingredients_db
)

from recipe.serializers import RecipeSerializer, RatingSerializer


class ListRecipe(ListAPIView):
    """Post one and get the list of all recipes"""
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        if self.request.query_params.get('name'):
            name = self.request.query_params.get('name')
            return list_recipes_name_db(name)

        if self.request.query_params.get('text'):
            text = self.request.query_params.get('text')
            return list_recipes_text_db(text)

        if self.request.query_params.get('ingredients'):
            ingredients = self.request.query_params.get('ingredients').split(',')
            return list_recipes_ingredients_db(ingredients)

        # in case maxingredient and miningredient in queryparams filter recipes
        # which have between or equal number of ingredients
        if self.request.query_params.get('maxingredient') and \
                self.request.query_params.get('miningredient'):
            maxingredient = self.request.query_params.get('maxingredient')
            miningredient = self.request.query_params.get('miningredient')
            return list_recipes_max_min_ingredients_db(maxingredient, miningredient)

        return list_recipes_db()

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user,
                            num_of_ingredients=len(request.data.get('ingredients')))
            return Response({'object': serializer.data},
                            status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors},
                            status.HTTP_400_BAD_REQUEST)


class RecipeDetails(APIView):
    """Get recipe details"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            recipe = get_recipe_db(id)
            if recipe:
                serializer = RecipeSerializer(instance=recipe)
                return Response(serializer.data, status.HTTP_200_OK)
        except Recipe.DoesNotExist:
            return Response({'errors': {'not_found': ['object does not exist']}},
                            status.HTTP_400_BAD_REQUEST)

# updating recipe not allowed

# deleting recipe not allowed


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_own_recipes(request):
    """List own recipes"""
    own_recipes = list_own_recipes_db(request.user)
    serializer = RecipeSerializer(own_recipes, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rate_recipe(request, id):
    """Rate recipes"""
    recipe = None

    try:
        recipe = get_recipe_db(id)
    except Recipe.DoesNotExist:
        return Response({'errors': {'not_found': ['object does not exist']}},
                        status.HTTP_400_BAD_REQUEST)

    if recipe.user == request.user:
        return Response ({'errors': 'cannot rate your own recipe'},
                        status.HTTP_400_BAD_REQUEST)

    serializer = RatingSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({'errors':
                         'rating not present or not integer between 1 and 5'},
                          status.HTTP_400_BAD_REQUEST)

    recipe_id = rate_recipe_db(recipe, request.data.get('rating'))
    resp = 'recipe {0} successfully rated'.format(recipe_id)
    return Response({'message': resp}, status.HTTP_200_OK)









