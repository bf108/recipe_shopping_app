from django.urls import path
from . import views
from .views import (RecipeDetailView, 
	RecipeListView,
    RecipeCreateView,
    RecipeUpdateView,
	IngredientCreateView,
	IngredientUpdateView,
	IngredientDeleteView)

urlpatterns = [
    path('',RecipeListView.as_view(), name='recipe_list'),
    path('recipe/update/<str:title>/<int:pk>/',RecipeUpdateView.as_view(),name='recipe_update'),
    path('create_recipe/',RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<str:title>/<int:pk>/',RecipeDetailView.as_view(),name='recipe_detail'),
    path('recipe/<str:title>/add_ingredient/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('recipe/<str:title>/update/<int:pk>/', IngredientUpdateView.as_view(), name='ingredient_update'),
    path('recipe/<str:title>/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient_delete'),


]