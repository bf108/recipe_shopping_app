from django.urls import path
from . import views
from .views import (RecipeDetailView, 
	RecipeListView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
	IngredientCreateView,
	IngredientUpdateView,
	IngredientDeleteView,
    ShoppingDetailView,
    ShoppingUpdateView,
    sendEmail,

    )

urlpatterns = [
    path('',RecipeListView.as_view(), name='recipe_list'),
    path('recipe/update/<str:title>/<int:pk>/',RecipeUpdateView.as_view(),name='recipe_update'),
    path('create_recipe/',RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<str:title>/<int:pk>/',RecipeDetailView.as_view(),name='recipe_detail'),
    path('recipe/<str:title>/delete/<int:pk>/',RecipeDeleteView.as_view(),name='recipe_delete'),
    path('recipe/<str:title>/add_ingredient/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('recipe/<str:title>/update/<int:pk>/', IngredientUpdateView.as_view(), name='ingredient_update'),
    path('recipe/<str:title>/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('shopping_list/<int:pk>/',ShoppingDetailView.as_view(), name='shoppingList_detail'),
    path('shopping_list/update/<int:pk>/',ShoppingUpdateView.as_view(), name='shoppingList_update'),
    path('shopping_list/sendEmail',sendEmail, name='sendEmail'),


]