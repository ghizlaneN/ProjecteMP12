from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)

def dict_get(dictionary, key):
    return dictionary.get(key)

@register.filter(name='add_class')

def add_class(value, arg):
    if hasattr(value, 'field') and hasattr(value.field, 'widget'):
        existing_classes = value.field.widget.attrs.get('class', '')
        # Evitar duplicar clases
        classes = existing_classes.split() if existing_classes else []
        if arg not in classes:
            classes.append(arg)
        value.field.widget.attrs['class'] = ' '.join(classes)
        return value
    return value
