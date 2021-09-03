from django.contrib.auth import get_user_model

from rest_framework import fields, serializers

from recipes.models import Ingredient, Recipe
from users.models import Favorite, Purchases, Subscription

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('title', 'dimension')


class PurchasesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchases
        fields = ('user', 'recipe')


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('user', 'author')


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
