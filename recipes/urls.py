from django.urls import path

from users.views import (download_purchases, purchases, favorite_recipe,
                         author_profile, subscriptions_list)

from . import views

app_name = 'recipes'

urlpatterns = [
    path('',
         views.index,
         name='index'),
    path('favorite/',
         favorite_recipe,
         name='favorite_recipes'),
    path('new-recipe/',
         views.new_recipe,
         name='new-recipe'),
    path('purchase/',
         purchases,
         name='purchases_list'),
    path('purchases-download/',
         download_purchases,
         name='purchases-download'),
    path("recipes/<int:recipe_id>/",
         views.recipe_view,
         name='recipe-view'),
    path("recipes/<int:recipe_id>/edit/",
         views.recipe_edit,
         name="recipe-edit"),
    path("recipes/<int:recipe_id>/delete/",
         views.recipe_delete,
         name="recipe-delete"),
    path('subscription/',
         subscriptions_list,
         name='user_subscriptions'),
    path('users/<str:username>/',
         author_profile,
         name='author-profile'),
]
