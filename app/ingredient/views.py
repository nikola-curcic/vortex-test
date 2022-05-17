import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ingredient.repository import (
                                    list_ingredients_db,
                                    get_ingredient_db,
                                    query_most_used_ingredients_db

)
from ingredient.serializers import IngredientSerializer


class ListIngredients(ListAPIView):
    """Post one and get the list of all ingredients"""
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return list_ingredients_db()

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'object': serializer.data},
                            status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors},
                            status.HTTP_400_BAD_REQUEST)


class IngredientDetails(APIView):
    """Get ingredient details"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            ingredient = get_ingredient_db(id)
            if ingredient:
                serializer = IngredientSerializer(instance=ingredient)
                return Response(serializer.data, status.HTTP_200_OK)
        except Ingredient.DoesNotExist:
            return Response({'errors': {'not_found': ['object does not exist']}},
                            status.HTTP_400_BAD_REQUEST)

# updating ingredient not allowed

# deleting ingredient not allowed


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_most_used_ingredients(request):
    """List most used ingredients"""
    ingredients = query_most_used_ingredients_db()
    return Response( {'most used ingredients': ingredients}, status.HTTP_200_OK)
