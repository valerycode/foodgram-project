from django import template

from recipes.models import Tag

register = template.Library()


@register.filter
def all_tags(value):
    return Tag.objects.all()


@register.filter
def get_active_tags(value):
    return value.getlist('tag')
