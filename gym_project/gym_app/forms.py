from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# Definim el formulari per iniciar sessió
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
# Definim el formulari per editar el perfil
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name']
        