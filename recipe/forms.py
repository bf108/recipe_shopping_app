from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from .models import ShoppingList, Recipe

#Customize the ModelMultipleChoiceField to alter dislay of recipe title only
class CustomMMCF(forms.ModelMultipleChoiceField):

	def label_from_instance(self, recipe):
		return f'{recipe.title}'

class CreateShoppingListForm(ModelForm):
	
	meals = CustomMMCF(
		widget = CheckboxSelectMultiple,
		queryset = Recipe.objects.all()
		)

	class Meta:
		model = ShoppingList
		fields = ['meals']

	# 	def __init__(self, *args, **kwargs):
	# 		super().__init__(*args, **kwargs)

	# 		self.fields['meals'].widget = CheckboxSelectMultiple()
	# 		self.fields['meals'].queryset = Recipe.objects.all()