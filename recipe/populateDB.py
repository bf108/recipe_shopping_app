import sys, os, django
import pandas as pd

sys.path.append('/Users/benfarrell/Desktop/shop_App')
os.environ["DJANGO_SETTINGS_MODULE"] =  "shop_App.settings"
django.setup()

from recipe.models import Recipe, Ingredient

# fishChips = Recipe.objects.create(title='Fish and Chips', description='Fried fish and chips.')

def createCookBook():

	xls = pd.ExcelFile('menus2.xlsx')
	tabs = pd.read_excel('menus2.xlsx', sheet_name=xls.sheet_names)

	for meal in tabs:
		if meal not in ['meals','in_stock']:
			rec = Recipe.objects.create(title=meal)

			for index in range(0,tabs[meal].shape[0]):
				row = tabs[meal].iloc[index]

				if type(row['units']) == str:
					Ingredient.objects.create(title=row['item'],qty=row['qty'],units=row['units'],recipe=rec)
				else:
					Ingredient.objects.create(title=row['item'],qty=row['qty'],recipe=rec)

createCookBook()