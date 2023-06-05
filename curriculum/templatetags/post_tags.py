from django import template

register = template.Library()

@register.filter(name='split')
def split(value,key):
    return value.split(key)

@register.filter(name='get_val')
def get_val(value,key):
    return "web Technologies"