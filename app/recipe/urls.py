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
    path('list-own-recepies',
         views.list_own_recepies,
         name='list_own_recepies')
]