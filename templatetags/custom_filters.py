from django import template

register = template.Library()

@register.filter(name='get_value')
def get_value(dictionary, key):
    """Returns the value of a given key from a dictionary."""
    return dictionary.get(key, None)
