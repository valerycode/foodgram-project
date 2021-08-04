from django.contrib import admin

from .models import Favorite, Purchases, Subscription


@admin.register(Favorite)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', )
    list_filter = ('user', 'recipe', )


@admin.register(Purchases)
class PurchasesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', )
    list_filter = ('user', 'recipe', )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', )
    list_filter = ('user', 'author', )
