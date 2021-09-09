from django import forms
from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        to_field_name='slug',
        required=False,
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.TextInput(attrs={"id": "nameIngredient"}),
        to_field_name='title',
        required=False
    )
    amount = []

    class Meta:
        model = Recipe
        fields = (
            'name',
            'tags',
            'ingredients',
            'cooking_time',
            'description',
            'image',
        )
        labels = {
            'name': 'Название рецепта',
            'tags': 'Теги',
            'ingredients': 'Ингредиенты',
            'cooking_time': 'Время приготовления',
            'description': 'Описание',
            'image': 'Загрузить фото',
        }

    def clean(self):
        tags_added = None
        ingredients_added = None
        for key in self.data.keys():
            if 'valueIngredient' in key:
                if int(self.data[key]) <= 0:
                    self.add_error(
                        'ingredients',
                        'Количество ингредиента должно быть больше 0')
            if 'nameIngredient' in key:
                ingredients_added = True
                if not Ingredient.objects.filter(
                        title=self.data[key]).exists():
                    self.add_error('ingredients',
                                   'Выберите ингредиент из списка')
            if 'tags' in key:
                tags_added = True
        if not tags_added:
            self.add_error('ingredients', 'Выберите тег/теги')
        if not ingredients_added:
            self.add_error('ingredients',
                           'Добавьте ингредиенты к вашему рецепту')

    def save_recipe(self, request, recipe):
        ingredients = self.get_ingredients(request)
        for title, amount in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            recipe_ing = RecipeIngredient(recipe=recipe,
                                          ingredient=ingredient,
                                          amount=amount)
            recipe_ing.save()

    def get_ingredients(self, request):
        ingredients = {}
        for key, title in request.POST.items():
            if 'nameIngredient' in key:
                elem = key.split("_")
                ingredients[title] = int(
                    request.POST[f'valueIngredient_{elem[1]}'])
        return ingredients
