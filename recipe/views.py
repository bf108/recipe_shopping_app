from django.shortcuts import render
from .models import Recipe, Ingredient
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

# Create your views here.

def listRecipe(request):

	recipes = Recipe.objects.all()

	return render(request,'recipe/home.html',context={'recipes':recipes})

class RecipeDetailView(DetailView):
	model = Recipe
	template_name = 'recipe/recipe_DetailView.html' #This is standard naming convention for class based view

def RecipeView(request, title):

	recipe = ' '.join(Recipe.objects.filter(title=title)[0].title.split('_'))

	pk = Recipe.objects.filter(title=title)[0].id
	ingredients = Ingredient.objects.filter(recipe_id=pk)

	context = {'recipe':recipe, 'ingredients':ingredients}

	return render(request, 'recipe/recipe_DetailView.html', context=context)

class IngredientCreateView(CreateView):
	model = Ingredient
	fields = ['title','qty','units']
	template_name = 'recipe/ingredient_add.html'

	def get_context_data(self, **kwargs):
		#Update get_context_data method to pass recipe title along with ingredient object to view/html template
		#This is the same as adding an argument to a view function
		#Get base context
		context = super().get_context_data(**kwargs)
		#Add a new key value pair to context dict
		context['recipe'] = self.kwargs['title']
		context['ingredients'] = Ingredient.objects.filter(recipe__title=self.kwargs['title'])
		return context
	
	def form_valid(self, form):
		#Update form_valid method to assign recipe to Foreign Key value of model.
		rec = Recipe.objects.filter(title=self.kwargs['title'])[0]
		form.instance.recipe = rec
		return super().form_valid(form)

	# def get_success_url(self):
	# 	return reverse('detail_recipe', kwargs={'title':self.Recipe.title})

class IngredientUpdateView(UpdateView):
	model = Ingredient
	fields = ['title','qty','units']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		#Add a new key value pair to context dict
		context['recipe'] = self.kwargs['title']
		context['ingredients'] = Ingredient.objects.filter(recipe__title=self.kwargs['title'])
		return context
	
	def form_valid(self, form):
		#Update form_valid method to assign recipe to Foreign Key value of model.
		rec = Recipe.objects.filter(title=self.kwargs['title'])[0]
		form.instance.recipe = rec
		return super().form_valid(form)

class IngredientDeleteView(DeleteView):
	model = Ingredient

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		#Add a new key value pair to context dict
		context['recipe'] = self.kwargs['title']
		context['ingredients'] = Ingredient.objects.filter(recipe__title=self.kwargs['title'])
		return context


	# To pass url variables to success url you have to modify/overwrite the get_success_url method 
	def get_success_url(self):
		return reverse_lazy('ingredient_create',kwargs={'title':self.kwargs['title']})

class RecipeCreateView(CreateView):
	model = Recipe
	fields = ['title','description']