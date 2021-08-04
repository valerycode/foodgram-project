from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    list_display = ('pk', 'recipe', 'ingredient', 'amount',)
    list_display_links = ('pk', 'recipe')
    list_filter = ('recipe', 'ingredient',)
    search_fields = ('ingredient__name', 'recipe',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    list_display_links = ('title',)
    inlines = [RecipeIngredientInline]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name')
    list_display_links = ('name',)
    search_fields = ('name', 'author', 'ingredient__name')
    inlines = [RecipeIngredientInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


admin.site.site_header = 'Foodgram'
admin.site.index_title = 'Административная панель'
