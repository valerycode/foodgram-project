from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FavoriteViewSet, IngredientViewSet, PurchaseViewSet,
                       SubscriptionViewSet)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(
    "ingredients",
    IngredientViewSet,
    basename="ingredients")
v1_router.register(
    "favorites",
    FavoriteViewSet,
    basename="favorites")
v1_router.register(
    "purchases",
    PurchaseViewSet,
    basename="purchases")
v1_router.register(
    "subscriptions",
    SubscriptionViewSet,
    basename="subscriptions")

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
