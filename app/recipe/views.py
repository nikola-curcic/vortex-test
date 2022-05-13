from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from core.models import Recipe
from recipe.serializers import RecipeSerializer


class ListIngredients(ListAPIView):
    """Post one and get the list of all recipes"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.get_queryset()

    def get_queryset(self):
        return self.queryset.all()

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'object': serializer.data},
                            status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors},
                            status.HTTP_400_BAD_REQUEST)


class RecipeDetails(APIView):

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
