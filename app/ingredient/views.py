from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from core.models import Ingredient
from ingredient.serializers import IngredientSerializer


class ListIngredients(ListAPIView):
    """Post one and get the list of all ingredients"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.get_queryset()
    authentication_classes = (TokenAuthentication,)
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
    authentication_classes = (TokenAuthentication,)
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
