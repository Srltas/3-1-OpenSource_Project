from django import template

register = template.Library()


@register.filter
def remainder(value, arg):
    return value % arg