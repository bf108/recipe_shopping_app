from django.urls import path
from . import views
from .views import RecipeDetailView, IngredientCreateView, IngredientUpdateView, IngredientDeleteView

urlpatterns = [
    path('', views.listRecipe, name='recipes'),
    # path('recipe/<int:pk>/',views.RecipeView, name='detail_recipe'),
    path('recipe/<str:title>/',views.RecipeView, name='detail_recipe'),
    path('recipe/<str:title>/add_ingredient/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('recipe/<str:title>/update/<int:pk>/', IngredientUpdateView.as_view(), name='ingredient_update'),
    path('recipe/<str:title>/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient_delete'),
    # path('recipe/<int:pk>/',RecipeDetailView.as_view(),name='detail_recipe'),

]