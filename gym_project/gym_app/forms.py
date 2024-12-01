from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Rutina

# Definim el formulari per registrar un nou usuari
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True) # format email i requerit
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        # Camps que es mostraran al formulari
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2']

# Definim el formulari per iniciar sessió
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
# Definim el formulari per editar el perfil
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name']
        
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