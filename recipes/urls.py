from django.urls import path

from users.views import (download_purchases, purchases_list,
                         favorite_recipe, author_profile, subscriptions_list)

from . import views

app_name = 'recipes'

urlpatterns = [
    path('subscription/',
         subscriptions_list,
         name='user_subscriptions'),
    path('favorite/',
         favorite_recipe,
         name='favorite_recipes'),
    path('purchase/',
         purchases_list,
         name='purchases_list'),
    path("recipes/<int:recipe_id>/",
         views.recipe_view,
         name='recipe-view'),
    path("recipes/<int:recipe_id>/edit/",
         views.recipe_edit,
         name="recipe-edit"),
    path("recipes/<int:recipe_id>/delete/",
         views.recipe_delete,
         name="recipe-delete"),
    path('new-recipe/',
         views.new_recipe,
         name='new-recipe'),
    path('users/<str:username>/',
         author_profile,
         name='author-profile'),
    path('purchases-download/',
         download_purchases,
         name='purchases-download'),
    path('',
         views.index,
         name='index'),
]
