from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from foodgram import settings

from pytils.translit import slugify

from .models import Ingredient, Recipe, RecipeIngredient, Tag
from .forms import RecipeForm


def index(request):
    tags = request.GET.getlist('tag')
    recipe_list = Recipe.objects.tag_filter(tags)
    paginator = Paginator(recipe_list, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/index.html', {
        'page': page,
        'paginator': paginator,
    })


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            "recipes/create_or_edit_recipe.html",
            {"form": form})
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.slug = slugify(recipe.name)
    recipe.save()
    return redirect("recipes:index")


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.recipe_ingredients.select_related().all()

    context = {
        'recipe': recipe,
        'ingredients': ingredients,
    }
    return render(
        request,
        'recipes/includes/recipe_card.html',
        context=context
    )


@login_required()
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipes:index')
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        form.save()
        return redirect('recipes:recipe-view', recipe_id)
    return render(request, 'recipes/create_or_edit_recipe.html', {
        "form": form,
        "recipe": recipe,
    })


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return redirect('recipes:recipe-view', recipe_id)
    recipe.delete()
    return redirect('recipes:index')
