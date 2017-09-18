from django import template

register = template.Library()

@register.filter
def kv(dict, key):    
    return dict[key]
