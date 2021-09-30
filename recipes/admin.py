from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Ingredient, Recipe, RecipeIngredient, Tag

AdminSite.empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    list_filter = ('title',)
    list_display_links = ('title',)
    inlines = [RecipeIngredientInline]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'favorites_count',)
    list_filter = ('author', 'name', 'tags',)
    readonly_fields = ("favorites_count",)
    list_display_links = ('name',)
    search_fields = ('name', 'author', 'ingredient__name',)
    inlines = [RecipeIngredientInline]
    add_fieldsets = (
        (
            None,
            {
                "fields": ("favorites_count",),
            },
        ),
    )

    def favorites_count(self, obj):
        return obj.favorite_recipe.count()

    favorites_count.short_description = "В избранном"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    search_fields = ("name", "slug",)


admin.site.site_header = 'Foodgram'
admin.site.index_title = 'Административная панель'
