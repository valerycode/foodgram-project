from django import template

from users.models import Favorite, Purchase, Subscription

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_favorite(recipe_id, user):
    return Favorite.objects.filter(user=user, recipe=recipe_id).exists()


@register.filter
def has_subscription(author_id, user):
    return Subscription.objects.filter(author=author_id, user=user).exists()


@register.filter
def in_purchases(recipe_id, user):
    return Purchase.objects.filter(user=user, recipe=recipe_id).exists()


@register.filter
def purchases_count(request):
    if not request.user.is_authenticated:
        return None
    return Purchase.objects.filter(user=request.user).count()
