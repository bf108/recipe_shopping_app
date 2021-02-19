from django.urls import path
from . import views
from .views import RecipeDetailView

urlpatterns = [
    path('', views.listRecipe, name='recipes'),
    path('recipe/<int:pk>/',views.RecipeView, name='detail_recipe'),
    # path('recipe/<int:pk>/',RecipeDetailView.as_view(),name='detail_recipe'),
]