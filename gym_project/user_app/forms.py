from djongo import models
from django import forms
from .models import Quotes

# Definim un formulari per a les quotes
class QuotesForm(forms.ModelForm):
    class Meta:
        # Assignem el model Quotes al formulari
        model = Quotes
        # Definim els camps que es mostren al formulari
        fields = ['quote_description']
        # Definim els labels dels camps
        labels = {
            'quote_description': 'Selecciona una quota'
        }