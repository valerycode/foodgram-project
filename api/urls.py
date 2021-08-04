from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (FavoriteViewSet, IngredientViewSet,
                       PurchasesViewSet, SubscriptionViewSet)
app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'ingredients', IngredientViewSet, basename='ingredients')
v1_router.register(r'favorites', FavoriteViewSet, basename='favorites')
v1_router.register(r'purchases', PurchasesViewSet, basename='purchases')
v1_router.register(r'subscriptions', SubscriptionViewSet,
                   basename='subscriptions')
urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
