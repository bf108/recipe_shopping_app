from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your models here.

# Relationship between ingredients and Recipe was considered.
# A ManyToMany relationship between ingredients and food would be possible if the ingredients didn't have quantities associated
# As qtys are required by ingredient it makes more sense for Recipes to form a OneToMany relationship.
# Each recipe links to many ingredients, but each ingredient only links to one recipe
# This will be done via a ForeignKey within Ingredient

class Recipe(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True,null=True)

	def __str__(self):
		return f'{self.title}: {self.description}'

	def get_absolute_url(self):
		return reverse('ingredient_create', kwargs={'title':self.title})

class Ingredient(models.Model):
	title = models.CharField(max_length=100)
	qty = models.FloatField(default=1)

	UnitType = models.TextChoices('UnitType','g ml tbsp tsp')
	units = models.CharField(blank=True,null=True,choices=UnitType.choices,max_length=5)

	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

	def __str__(self):
		if self.units:
			text = f'{self.title}: {self.qty}{self.units}'
		else:
			text = f'{self.title}: {self.qty}'

		return text

	def get_absolute_url(self):
		return reverse('ingredient_create', kwargs={'title':self.recipe.title})

class ShoppingList(models.Model):
	user = models.OneToOneField(
		get_user_model(),
		primary_key=True,
		on_delete=models.CASCADE)

	meals = models.ManyToManyField(Recipe, blank=True, null=True)