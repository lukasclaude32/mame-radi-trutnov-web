from django import template

register = template.Library()


@register.filter
def widget_type(field):
    """Return the widget class name for a form field."""
    return field.field.widget.__class__.__name__


@register.filter
def input_type(field):
    """Return the input type for a form field."""
    return getattr(field.field.widget, 'input_type', 'text')
