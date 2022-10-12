from django import template

register = template.Library()

@register.simple_tag
def underscoreTag(obj, attribute):
    obj = obj.attribute
    return obj.attribute


