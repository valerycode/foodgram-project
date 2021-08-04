from django.urls import path

from users.views import (purchases_list,
                         favorite_recipe, author_recipes, subscriptions_list)

from . import views

app_name = 'recipes'

urlpatterns = [
    path('subscriptions/',
         subscriptions_list,
         name='subscriptions'),
    path('favorites/',
         favorite_recipe,
         name='favorites'),
    path('purchases/',
         purchases_list,
         name='purchases'),
    path("<int:pk>/detail/",
         views.recipe_delete,
         name="recipe-delete"),
    path('new-recipe/',
         views.new_recipe,
         name='new-recipe'),
    path("<int:pk>/edit/",
         views.recipe_edit,
         name="recipe-edit"),
    path("<int:pk>/",
         views.recipe_view,
         name='recipe-view'),
    path('<str:username>/',
         author_recipes,
         name='author-recipes'),
    # path('purchases-download/',
    #      download_purchases,
    #      name='purchases-download')
    path('',
         views.index,
         name='index'),
]
