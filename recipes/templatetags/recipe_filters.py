from django import template

from recipes.models import Tag

register = template.Library()


@register.filter
def all_tags(value):
    return Tag.objects.all()


@register.filter
def get_active_tags(value):
    return value.getlist('tag')


@register.filter
def change_tag_link(request, tag):
    copy = request.GET.copy()
    if copy.getlist('page'):
        copy.pop('page')
    tag_link = copy.getlist('tag')
    if tag.slug in tag_link:
        while tag.slug in tag_link:
            tag_link.remove(tag.slug)
        copy.setlist('tag', tag_link)
    else:
        copy.appendlist('tag', tag.slug)
    return copy.urlencode()


@register.filter
def subtract(num1, num2):
    return num1 - num2


@register.filter
def ru_pluralize(value, words):
    args = words.split(',')
    number = abs(int(value))
    a = number % 10
    b = number % 100
    if a == 1 and b != 11:
        return args[0]
    if 2 <= a <= 4 and b < 10 or b >= 20:
        return args[1]
    return args[2]


@register.simple_tag
def set_page(request, value):
    request_object = request.GET.copy()
    request_object['page'] = value
    return request_object.urlencode()
