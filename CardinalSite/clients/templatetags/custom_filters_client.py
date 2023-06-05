from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def format_number_with_commas(value):
    try:
        value = float(value)
        return "{:,.2f}".format(value)
    except (TypeError, ValueError):
        return value
