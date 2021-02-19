from django.shortcuts import render
from .models import Recipe, Ingredient
from django.views.generic import DetailView, CreateView, UpdateView

# Create your views here.

def listRecipe(request):

	recipes = Recipe.objects.all()

	return render(request,'recipe/home.html',context={'recipes':recipes})

class RecipeDetailView(DetailView):
	model = Recipe
	template_name = 'recipe/recipe_DetailView.html' #This is standard naming convention for class based view

def RecipeView(request, pk):

	recipe = ' '.join(Recipe.objects.filter(id=pk)[0].title.split('_'))
	ingredients = Ingredient.objects.filter(recipe_id=pk)

	context = {'recipe':recipe, 'ingredients':ingredients}

	return render(request, 'recipe/recipe_DetailView.html', context=context)