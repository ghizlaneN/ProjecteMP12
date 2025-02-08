from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    # Filtre personalitzat per obtenir un element d'un diccionari
    return dictionary.get(key)


def dict_get(dictionary, key):
    # Funció auxiliar per obtenir un element d'un diccionari
    return dictionary.get(key)