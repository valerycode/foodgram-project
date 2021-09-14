from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated,)

from recipes.models import Ingredient, Recipe
from users.models import Favorite, Purchase, Subscription
from .serializers import (IngredientSerializer,
                          PurchaseSerializer,
                          SubscriptionSerializer,
                          FavoriteSerializer)

User = get_user_model()


class CreateDeleteGeneric(mixins.DestroyModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        if 'id' not in request.data:
            return Response(
                {"success": False}, status=status.HTTP_400_BAD_REQUEST,
                )
        data = {}
        if self.lookup_field == "recipe":
            recipe = get_object_or_404(Recipe, pk=request.data["id"])
            data = {
                'user': request.user.id,
                'recipe': recipe.id,
            }
        elif self.lookup_field == "author":
            author = get_object_or_404(User, pk=request.data["id"])
            data = {
                'user': request.user.id,
                'author': author.id,
            }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse({"success": True}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            data={'success': True},
            status=status.HTTP_200_OK
        )


class PurchaseViewSet(CreateDeleteGeneric, mixins.ListModelMixin):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'recipe'


class SubscriptionViewSet(CreateDeleteGeneric):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'author'


class FavoriteViewSet(CreateDeleteGeneric, mixins.ListModelMixin):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'recipe'


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']
