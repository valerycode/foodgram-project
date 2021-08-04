from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy

from foodgram import settings

from recipes.models import Recipe, Tag

from .models import Favorite, Purchases, Subscription
from .forms import CreationForm

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class UserPasswordReset(PasswordResetView):
    from_email = settings.EMAIL_HOST_USER


@login_required
def subscriptions_list(request):
    user_subscriptions = Subscription.objects.filter(user=request.user)
    paginator = Paginator(user_subscriptions, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if page:
        return render(request, 'recipes/subscriptions.html', {
            'page': page,
            'paginator': paginator,
        })
    return render(request, 'recipes/custom_page.html')


@login_required
def favorite_recipe(request):
    user = get_object_or_404(User, username=request.user)
    recipes = Favorite.objects.prefetch_related(
        '"favorite__tag', 'favorite_subscriber'
    ).filter(user=user)
    tags = request.GET.getlist('tags')
    if tags:
        recipes = Favorite.objects.filter(
            favorite__tag__slug__in=tags, user=user).distinct()
    all_tags = Tag.objects.all()
    paginator = Paginator(recipes, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'all_tags': all_tags,

        }
    return render(request, 'recipes/favorite.html', context=context)


@login_required
def purchases_list(request):
    purchases_list = Purchases.objects.select_related(
        'recipe').filter(
        user=request.user.id
    )
    context = {
        'purchases_list': purchases_list,
    }
    return render(request, 'recipes/purchases.html', context=context)


def author_recipes(request, username):
    tags = request.GET.getlist('tags')
    author = get_object_or_404(User, username=username)
    recipes = author.author_recipes.all()
    if tags:
        recipes = Recipe.objects.filter(
            tag__slug__in=tags, author=author).distinct()
    paginator = Paginator(recipes, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/author_recipes.html', {
        'author': author,
        'page': page,
        'paginator': paginator,
    })
