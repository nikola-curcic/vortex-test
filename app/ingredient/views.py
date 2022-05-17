import json

from django.db import connection

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Ingredient
from ingredient.serializers import IngredientSerializer


class ListIngredients(ListAPIView):
    """Post one and get the list of all ingredients"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.get_queryset()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()

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
            ingredient = Ingredient.objects.get(id=id)
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
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT ci.name, COUNT(*) AS number '
            'FROM core_recipe_ingredients crp '
            'LEFT JOIN core_ingredient ci '
            'ON ci.id = crp.ingredient_id '
            'GROUP BY ci.name '
            'ORDER BY number DESC '
            'LIMIT 5'
        )
        data = cursor.fetchall()

        ingredients = [{'name': d[0], 'number_of_recipes': d[1]} for d in data]

    return Response( {'most used ingredients': ingredients}, status.HTTP_200_OK)
