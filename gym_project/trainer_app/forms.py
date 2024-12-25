from django import forms
from .models import Rutina

class CrearRutinaForm(forms.ModelForm):
    class Meta:   
        model = Rutina
        fields = ['nom', 'descripcio', 'exercicis', 'recomenacions']
        
class EditRutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['descripcio', 'exercicis', 'recomenacions']
        
class HorariForm(forms.Form):
    rutinas = forms.ModelChoiceField(queryset=Rutina.objects.all(), required=False, empty_label="Selecciona rutina")