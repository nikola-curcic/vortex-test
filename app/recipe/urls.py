from django.urls import path
from recipe import views

app_name = 'recipe'

urlpatterns = [
    path('',
         views.ListIngredients.as_view(),
         name='recipes'),
    path('<int:id>',
         views.RecipeDetails.as_view(),
         name='ingredients')
]