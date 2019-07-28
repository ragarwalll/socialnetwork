from django import template

register = template.Library()


@register.filter(name='check')
def check(value, args):
    find = value.filter(user_liked=args)
    return 1 if find else 0
