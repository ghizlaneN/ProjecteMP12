from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    """Afegir una classe al widget."""
    if hasattr(value, 'field') and hasattr(value.field, 'widget'):
        existing_classes = value.field.widget.attrs.get('class', '')
        # Evitar duplicar clases
        classes = existing_classes.split() if existing_classes else []
        if arg not in classes:
            classes.append(arg)
        value.field.widget.attrs['class'] = ' '.join(classes)
        return value
    return value

def get_item(dictionary, key):
    return dictionary.get(key)
