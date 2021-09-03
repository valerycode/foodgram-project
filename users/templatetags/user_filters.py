from django import template

from users.models import Favorite, Purchases, Subscription

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_favorite(recipe_id, user):
    """Проверяет добавлен ли рецепт в избранное"""
    return Favorite.objects.filter(user=user, recipe=recipe_id).exists()


@register.filter
def has_subscription(author_id, user):
    """Проверяет подписан ли текущий пользователь на автора"""
    return Subscription.objects.filter(author=author_id, user=user).exists()


@register.filter
def in_purchases(recipe_id, user):
    """Проверяет добавлен ли рецепт в список покупок"""
    return Purchases.objects.filter(user=user, recipe=recipe_id).exists()


@register.filter
def purchases_count(request):
    """Считает количество добавленных рецептов в список покупок"""
    if request.user.is_authenticated:
        return Purchases.objects.filter(user=request.user).count()
