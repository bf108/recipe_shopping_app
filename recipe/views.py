from django.shortcuts import render, get_object_or_404
from .models import Recipe, Ingredient, ShoppingList
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse, reverse_lazy
from .forms import CreateShoppingListForm

# Create your views here.

def listRecipe(request):

	recipes = Recipe.objects.all()

	return render(request,'recipe/home.html',context={'recipes':recipes})

class RecipeListView(ListView):
	model = Recipe

class RecipeDetailView(DetailView):
	model = Recipe
	template_name = 'recipe/recipe_DetailView.html' #This is standard naming convention for class based view

class RecipeCreateView(CreateView):
	model = Recipe
	fields = ['title','description']

class RecipeUpdateView(UpdateView):
	model = Recipe
	fields = ['title','description']

class RecipeDeleteView(DeleteView):
	model = Recipe

	# To pass url variables to success url you have to modify/overwrite the get_success_url method 
	def get_success_url(self):
		return reverse_lazy('recipe_list')

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
		context['pk'] = Recipe.objects.filter(title=self.kwargs['title'])[0].id
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
		context['pk'] = Recipe.objects.filter(title=self.kwargs['title'])[0].id
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

class ShoppingDetailView(DetailView):
	model = ShoppingList
	template_name = 'recipe/spl_DetailView.html'

	def get_context_data(self, **kwargs):
		#Update get_context_data method to pass recipe title along with ingredient object to view/html template
		#This is the same as adding an argument to a view function
		#Get base context
		context = super().get_context_data(**kwargs)
		context['new'] = 'RandomText'
		recipes = [rec.title for rec in ShoppingList.objects.get(pk=self.kwargs['pk']).meals.all()]

		toBuy = dict()

		for recipe in recipes:
			for ingredient in Ingredient.objects.filter(recipe__title=recipe).all():
				if ingredient.title.lower() in toBuy:
					toBuy[ingredient.title.lower()]["qty"]+=ingredient.qty
				else:
					toBuy[ingredient.title.lower()] = {"qty":ingredient.qty,"units":ingredient.units}

		context['ingredients'] = toBuy

		return context

class ShoppingUpdateView(UpdateView):
	model = ShoppingList
	form_class = CreateShoppingListForm
	# fields = ['meals']

	def get_success_url(self):
		return reverse('shoppingList_detail', kwargs={'pk':self.kwargs['pk']})