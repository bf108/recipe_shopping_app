from django.contrib import admin
from .models import Recipe, Ingredient, ShoppingList
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)

class ShoppingListAdmin(admin.ModelAdmin):
	formfield_overrides = {models.ManyToManyField: {'widget': CheckboxSelectMultiple}}

admin.site.register(ShoppingList, ShoppingListAdmin)