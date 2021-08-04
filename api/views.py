from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import filters, mixins, viewsets

from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,)

from recipes.models import Ingredient
from users.models import Favorite, Purchases, Subscription

from .serializers import (IngredientSerializer,
                          PurchasesSerializer,
                          SubscriptionSerializer,
                          FavoritesSerializer)

CreateListDeleteGeneric = (mixins.DestroyModelMixin, mixins.CreateModelMixin,
                           mixins.ListModelMixin, viewsets.GenericViewSet)


class PurchasesViewSet(*CreateListDeleteGeneric):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = (IsAuthenticated,)


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,#для теста
                          viewsets.GenericViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(
            queryset=Subscription.objects.all(),
            user=self.request.user,
            author__id=self.kwargs.get('pk')
        )


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.RetrieveModelMixin, #для теста
                      mixins.ListModelMixin, #для теста
                      viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = (IsAuthenticated,)


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^title',)
