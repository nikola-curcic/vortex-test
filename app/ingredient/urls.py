from django.urls import path
from ingredient import views

app_name = 'ingredient'

urlpatterns = [
    path('',
         views.ListIngredients.as_view(),
         name='ingredients'),
    path('<int:id>',
         views.IngredientDetails.as_view(),
         name='ingredients'),
    path('list-most-used-ingredients/',
         views.list_most_used_ingredients,
         name='list_most_used_ingredients')
]
