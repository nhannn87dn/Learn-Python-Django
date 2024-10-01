# myapp/templatetags/form_tags.py
from django import template

register = template.Library()

# Tiện ích add thêm class cho thẻ

@register.filter(name='add_class')
def add_class(field, css_class):
    if hasattr(field, 'field'):
        field.field.widget.attrs['class'] = field.field.widget.attrs.get('class', '') + ' ' + css_class
    else:
        field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' ' + css_class
    return field