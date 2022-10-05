import datetime
from decimal import Decimal

from django import template

register = template.Library()


@register.filter("startswith")
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter("isdate")
def isdate(val):
    return isinstance(val, datetime.date)


@register.filter("isbool")
def isbool(val):
    return isinstance(val, bool)


@register.filter("isdecimal")
def isdecimal(val):
    return isinstance(val, Decimal)


@register.filter("datevalue")
def datevalue(val):
    date = datetime.datetime.strptime(val, "%Y-%m-%d").date()
    return date


@register.filter("get_query_parameters")
def get_query_parameters(val):
    if val:
        result = "?"
        for key, value in val.items():
            result += f"{key}={value}&"
        result = result[0:-1]
        return result
    return val


@register.filter("get_value_dict")
def get_value_dict(dictionary, key):
    return dictionary.get(key)
