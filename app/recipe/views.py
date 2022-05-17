from django.core import serializers
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Recipe
from recipe.serializers import RecipeSerializer, RatingSerializer


class ListRecipe(ListAPIView):
    """Post one and get the list of all recipes"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.get_queryset()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
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
            recipe = Recipe.objects.get(id=id)
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
    """List own recepies"""
    own_recipes = list(Recipe.objects.filter(user=request.user))
    serializer = RecipeSerializer(own_recipes, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rate_recipe(request, id):
    """Rate recipes"""
    recipe = None

    try:
        recipe = Recipe.objects.get(id=id)
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

    num_of_ratings = recipe.num_of_ratings + 1
    total_rating = recipe.total_rating + request.data.get('rating')
    average_rating = total_rating/num_of_ratings
    recipe.total_rating = total_rating
    recipe.average_rating = average_rating
    recipe.num_of_ratings = num_of_ratings
    recipe.save()
    return Response({'message': 'recipe succesfully rated'}, status.HTTP_200_OK)









