from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from foodgram import settings
from recipes.models import Recipe

from .forms import CreationForm
from .models import Favorite, Purchases, Subscription

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class UserPasswordReset(PasswordResetView):
    from_email = settings.EMAIL_HOST_USER


@login_required
def subscriptions_list(request):
    user_subscriptions = Subscription.objects.subscriptions(user=request.user)
    paginator = Paginator(user_subscriptions, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'recipes/subscriptions.html', context=context)


@login_required
def favorite_recipe(request):
    tags = request.GET.getlist('tag')
    favorite_list = Favorite.objects.favorite_recipe(request.user, tags)
    paginator = Paginator(favorite_list, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/favorite.html', {
            'page': page,
            'paginator': paginator,
        })


@login_required
def purchases(request):
    purchases_list = Purchases.objects.select_related(
        'recipe').filter(
        user=request.user.id
    )
    context = {
        'purchases_list': purchases_list,
    }
    return render(request, 'recipes/purchases.html', context=context)


@login_required
def download_purchases(request):
    recipes = Recipe.objects.filter(purchases_recipe__user=request.user)
    ingredients = recipes.values(
        'ingredients__title', 'ingredients__dimension',
    ).annotate(
        Sum('recipe_ingredients__amount')).order_by()

    content = ''

    for item in ingredients:
        right_position_item = (
            item.get('ingredients__title'),
            str(item.get('recipe_ingredients__amount__sum')),
            item.get('ingredients__dimension')
        )
        content += ' '.join(right_position_item) + '\n'

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=shopping-list.txt'
    return response


def author_profile(request, username):
    tags = request.GET.getlist('tag')
    author = get_object_or_404(User, username=username)
    post_list = Recipe.objects.tag_filter(tags).filter(author=author)
    paginator = Paginator(post_list, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/author_profile.html', {
        'author': author,
        'page': page,
        'paginator': paginator,
    })
