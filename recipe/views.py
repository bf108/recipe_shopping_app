from django.shortcuts import render

# Create your views here.

def listRecipe(request):

	recipes = ['Sausage & Mash','Pizza','Pasta']

	return render(request,'recipe/home.html',context={'recipes':recipes})
