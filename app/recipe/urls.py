from django.urls import path
from recipe import views

app_name = 'recipe'

urlpatterns = [
    path('',
         views.ListRecipe.as_view(),
         name='recipes'),
    path('<int:id>',
         views.RecipeDetails.as_view(),
         name='ingredients'),
    path('list-own-recipes',
         views.list_own_recipes,
         name='list_own_recipes'),
    path('rate-recipe/<int:id>',
         views.rate_recipe,
         name='rate_recipe')
]