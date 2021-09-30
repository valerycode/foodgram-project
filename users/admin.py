from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Favorite, Purchase, Subscription


@admin.register(Favorite)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', )
    list_filter = ('user', 'recipe', )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', )
    list_filter = ('user', 'recipe', )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', )
    list_filter = ('user', 'author', )


class UserAdminCustom(UserAdmin):
    list_filter = ("username", "email")
    search_fields = ("username", "email")


admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)
