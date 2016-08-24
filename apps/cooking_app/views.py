from django.shortcuts import render, redirect, reverse
from .models import User, Comment, Recipe, Ingredient, Measurement, Step
from django.contrib import messages
import datetime

# Create your views here.
def login(request):
	if request.method == "POST" and User.objects.LoginValidation(request):
		return redirect(reverse('potluck:index'))
	return render(request, 'cooking_app/login.html')


def register(request):
	if request.method == "POST" and User.objects.RegisterValidation(request):
		return redirect(reverse('potluck:index'))
	return render(request, 'cooking_app/register.html')


def index(request):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))
	return render(request, 'cooking_app/index.html', {'user': User.objects.get(id=request.session['id'])})


def show_recipe(request, id):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	if request.method == 'POST':
		return redirect(reverse('potluck:create'))
	return render(request, 'cooking_app/show_recipe.html')\


def add_recipe(request):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	if request.method == 'POST': # if 'POST' we are trying to add something, else trying to display form to add
		if not Recipe.objects.validateRecipe(request): #run validations. returns false if failed
			return redirect(reverse('potluck:add_recipe'))
		#create the recipe if validations passed
		recipe = Recipe.objects.create(title=request.POST['title'], creator=User.objects.get(id=request.session['id']), description=request.POST['description'], prep_time_hour=request.POST['prep_time_hour'], prep_time_minute=request.POST['prep_time_minute'], cook_time_hour=request.POST['cook_time_hour'], cook_time_minute=request.POST['cook_time_minute'])
		#redirect to edit page so user can add steps to recipe
		return redirect(reverse('potluck:edit_recipe', kwargs={'recipe_id': recipe.id}))
	return render(request, 'cooking_app/add_recipe.html', {'user': User.objects.get(id=request.session['id'])})


def edit_recipe(request, recipe_id):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	if request.method == 'POST': # if 'POST' we are trying to update recipe, else trying to display edit page
		if not Recipe.objects.validateRecipe(request): # run validations. returns false if failed
			return redirect(reverse('potluck:edit_recipe'))
		else:
			Recipe.objects.update(request, recipe_id) # passed validation, not update

	# test if there are any steps for this recipe and pass them if so
	if len(Step.objects.filter(recipe=Recipe.objects.get(id=recipe_id)))>0:
		steps = Step.objects.filter(recipe=Recipe.objects.get(id=recipe_id))
		step_count = steps.count() + 1
	else: # otherwise, pass empty list rather than none (so traversing in the template doesnt cause an error)
		steps = []
		step_count = 1
	return render(request, 'cooking_app/edit_recipe.html', {'user': User.objects.get(id=request.session['id']),'recipe': Recipe.objects.get(id=recipe_id), 'steps':steps, 'step_count': step_count, 'ingredients': Ingredient.objects.all(), 'measurements': Measurement.objects.all()})


def add_step(request):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	step = Step.objects.add_step(request) # runs code to validate step and return step after creation
	return redirect(reverse('potluck:edit_recipe', kwargs={'recipe_id': step.recipe.id}))


def update_step(request, step_id):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	step = Step.objects.update_step(request, step_id) # runs code to validate step and return step after update
	return redirect(reverse('potluck:edit_recipe', kwargs={'recipe_id': step.recipe.id}))


def show_user(request, id):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	#TODO pass in user and recipes

	return render(request, 'cooking_app/show_user.html', {'user': User.objects.get(id=id)})


def logout(request):
	for key in request.session.keys():
		del request.session[key]
	return redirect(reverse('potluck:login'))









#
