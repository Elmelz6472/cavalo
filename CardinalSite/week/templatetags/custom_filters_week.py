from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def multiply_values(value1, value2):
    try:
        return value1 * value2
    except (TypeError, ValueError):
        return 0
    except VariableDoesNotExist:
        return 0