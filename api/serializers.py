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
    recipe = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Purchases
        fields = ('user', 'recipe')


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
     )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
     )

    class Meta:
        model = Subscription
        fields = ('user', 'author')


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        # fields = ('name',)
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer()
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
     )

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
