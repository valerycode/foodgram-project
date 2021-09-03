from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, viewsets
from rest_framework import status

from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated,)

from recipes.models import Ingredient, Recipe
from users.models import Favorite, Purchases, Subscription

from .serializers import (IngredientSerializer,
                          PurchasesSerializer,
                          SubscriptionSerializer,
                          FavoritesSerializer)

User = get_user_model()

CreateDeleteGeneric = (mixins.DestroyModelMixin, mixins.CreateModelMixin,
                       viewsets.GenericViewSet)


class CreateListDeleteGeneric(mixins.DestroyModelMixin,
                              mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=request.data["id"])
        data = {
            'user': request.user.id,
            'recipe': recipe.id,
        }
        request.data.update(data)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(
            data={'success': True},
            status=status.HTTP_200_OK
        )


class PurchasesViewSet(CreateListDeleteGeneric):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Purchases.objects.all(),
            user=self.request.user,
            recipe__id=self.kwargs.get('pk')
        )


class SubscriptionViewSet(*CreateDeleteGeneric):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=request.data["id"])
        data = {
            'user': request.user.id,
            'author': author.id,
        }
        request.data.update(data)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            data={'success': True},
            status=status.HTTP_200_OK
        )

    def get_object(self):
        return get_object_or_404(
            Subscription.objects.all(),
            user=self.request.user,
            author__id=self.kwargs.get('pk')
        )


class FavoriteViewSet(CreateListDeleteGeneric):
    queryset = Favorite.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Favorite.objects.all(),
            user=self.request.user,
            recipe__id=self.kwargs.get('pk')
        )


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']
