from django import forms
from .models import Rutina

# Formulari per crear una nova rutina
class CrearRutinaForm(forms.ModelForm):
    class Meta:   
        model = Rutina
        fields = ['nom', 'descripcio', 'exercicis', 'recomenacions']

# Formulari per editar una rutina existent
class EditRutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['descripcio', 'exercicis', 'recomenacions']

# Formulari per gestionar l'horari de les rutines
class HorariForm(forms.Form):
    # Camp per seleccionar una rutina existent
    rutinas = forms.ModelChoiceField(queryset=Rutina.objects.all(), required=False, empty_label="Selecciona rutina")