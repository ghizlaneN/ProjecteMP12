from django import forms
from gym_app.models import User
from user_app.models import Quotes
from django.contrib.auth.forms import UserCreationForm

# Formulari per editar usuaris
class EditUserForm(forms.ModelForm):

    # Camp per seleccionar la descripció de la quota
    quote_description = forms.ChoiceField(
        choices=Quotes.descripcio,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role']

    def __init__(self, *args, **kwargs):
        # Obtenim el rol d'usuari i la quota inicial dels arguments
        user_role = kwargs.pop('user_role', None)
        initial_quote = kwargs.pop('initial_quote', None)
        super().__init__(*args, **kwargs)

        # Eliminem el camp de quota si l'usuari no és un usuari normal
        if user_role != 'user':
            self.fields.pop('quote_description', None)

        # Establim la quota inicial si s'ha proporcionat
        if initial_quote is not None:
            self.fields['quote_description'].initial = initial_quote

# Formulari per registrar nous usuaris
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        # Camps que es mostraran al formulari
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2']