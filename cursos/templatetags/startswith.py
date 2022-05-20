import datetime

from django import template

register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter('isdate')
def isdate(val):
    return isinstance(val, datetime.date)


@register.filter('isbool')
def isbool(val):
    return isinstance(val, bool)
