from django.shortcuts import render, get_object_or_404
from .models import Recipe, Ingredient, ShoppingList
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse, reverse_lazy
from .forms import CreateShoppingListForm
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseRedirect
from shop_App.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


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
	fields = ['title','qty','units','food_type']
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
	fields = ['title','qty','units','food_type']

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

#Helper function to group ingredients in Shopping List
def groupIngredients(recipes):
	'''
	Group ingredients by food type

	args: recipes (type: list) - List of recipes in shopping list
	
	returns: Dict in format: {'food_type': {'Ingredient': {'qty':x, 'units':7} } }

	'''

	toBuy = dict()

	for recipe in recipes:
		for ingredient in Ingredient.objects.filter(recipe__title=recipe).all():
			if ingredient.food_type in toBuy:
				if ingredient.title.lower() in toBuy[ingredient.food_type]:
					toBuy[ingredient.food_type][ingredient.title.lower()]["qty"]+=ingredient.qty
				else:
					toBuy[ingredient.food_type][ingredient.title.lower()] = {
					"qty":ingredient.qty,
					"units":ingredient.units
					}
			else:
				toBuy[ingredient.food_type] = {ingredient.title.lower():{
				"qty":ingredient.qty,
				"units":ingredient.units
				}
				}

	return toBuy

def groupListIngredients(recipes):
	toBuy = dict()

	for recipe in recipes:
		for ingredient in Ingredient.objects.filter(recipe__title=recipe).all():
			if ingredient.food_type in toBuy:
				if ingredient.title.lower() in toBuy[ingredient.food_type]:
					toBuy[ingredient.food_type][ingredient.title.lower()]["qty"]+=ingredient.qty
				else:
					toBuy[ingredient.food_type][ingredient.title.lower()] = {
					"qty":ingredient.qty,
					"units":ingredient.units
					}
			else:
				toBuy[ingredient.food_type] = {ingredient.title.lower():{
				"qty":ingredient.qty,
				"units":ingredient.units
				}
				}

	toBuyList = []

	for foodType in toBuy:
		toBuyList.append(foodType)
		for ing in toBuy[foodType]:
			text = str(ing) + str(':')
			text += str(toBuy[foodType][ing]['qty'])
			text += str(toBuy[foodType][ing]['units'])
			toBuyList.append(text)

	return toBuyList

class ShoppingDetailView(DetailView):
	model = ShoppingList
	template_name = 'recipe/spl_DetailView.html'

	def get_context_data(self, **kwargs):
		#Update get_context_data method to pass recipe title along with ingredient object to view/html template
		#This is the same as adding an argument to a view function
		#Get base context
		context = super().get_context_data(**kwargs)
		
		recipes = [rec.title for rec in ShoppingList.objects.get(pk=self.kwargs['pk']).meals.all()]

		context['recipes'] = recipes

		context['ingredients'] = groupIngredients(recipes)

		context['ingredient_list'] = groupListIngredients(recipes)

		return context

class ShoppingUpdateView(UpdateView):
	model = ShoppingList
	form_class = CreateShoppingListForm

	def get_success_url(self):
		return reverse('shoppingList_detail', kwargs={'pk':self.kwargs['pk']})

def sendEmail(request):
	'''
	This function/view performs 3 distinct things:
	1. Creates a dict toBuy which groups ingredients by food type. 
	{'food_type':
		{'Ingredient':
				{'qty':x, 'units':7}
		}
	}

	2. Create email body with contents of toBuy dict
	3. Group and sorted contents of shopping list are emailed to users.

	'''
	recipes = [rec.title for rec in ShoppingList.objects.get(pk=request.user.id).meals.all()]

	def createEmailBody():

		toBuy = groupIngredients(recipes)

		msg_content = []

		for key in toBuy:
			msg_content.append(key)
			for ing, val in toBuy[key].items():
				if val.get('units') == None:
					comb = f'{ing}: {val.get("qty")}'
				else:
					comb = f'{ing}: {val.get("qty")}{val.get("units")}'
				
				msg_content.append(comb)

			msg_content.append('\n')

		msg_content = '\n'.join(msg_content)

		return msg_content
	
	send_mail(
		'This weeks shopping list!',
		createEmailBody(),
		'farrellben2020@gmail.com',
		['ben.farrell08@gmail.com',],
		# ['ben.farrell08@gmail.com','maddieross@gmail.com'],
		fail_silently=False,
		)

	messages.add_message(request, messages.SUCCESS, 'Shopping list emailed to Ben & Maddie!')

	return HttpResponseRedirect(reverse('shoppingList_detail',args=[request.user.id]))

def sendEmailAjax(request):

	if request.method == 'POST':

		content = request.POST.get('todoList')
		recipientList = request.POST.get('recipientList').split('\n')

		#Avoid requirements to include our emails every week.
		if len(recipientList) == 0:
			recipientList = ['ben.farrell08@gmail.com','maddieross@gmail.com']

		send_mail(
			'This weeks shopping list!',
			content,
			'farrellben2020@gmail.com',
			recipientList,
			fail_silently=False,
			)

		todos = request.POST.get('todoList',"Couldn't Find it")

		messages.add_message(request, messages.SUCCESS, f'Received Posted Data: {todos}')

		return HttpResponseRedirect(reverse('shoppingList_detail',args=[request.user.id]))

	else:
		messages.add_message(request, messages.WARNING, 'Didn\'t receive any Posted Data')

		return HttpResponseRedirect(reverse('shoppingList_detail',args=[request.user.id]))
