from django.urls import path
from ingredient import views

app_name = 'ingredient'

urlpatterns = [
    path('',
         views.ListIngredients.as_view(),
         name='ingredients'),
    path('<int:id>',
         views.IngredientDetails.as_view(),
         name='ingredients')
]
