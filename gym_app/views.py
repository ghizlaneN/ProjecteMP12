from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm
from django.contrib.auth.forms import UserChangeForm


# Create your views here.
# Definim la pàgina per editar el perfil de l'usuari, que es crida quan es visita la url '/editar_perfil/'
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # Si el formulari és correcte, registrem l'usuari i iniciem la sessió sino mostrarà un missatge d'error
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "El registre s'ha completat correctament!")
            return redirect('home')
        else:
            messages.error(request, "No s'ha pogut completar el registre. Torneu-ho a intentar.")
    else:
        # Si no es POST, creem un nou formulari per registrar-se
        form = UserRegistrationForm()
    return render(request, 'gym_app/register.html', {'form': form})
# Definim la pàgina per iniciar sessió, que es crida quan es visita la url '/login/'
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Obtenim el email i la contrasenya dels camps del formulari
            email = form.cleaned_data.get('email') 
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            # Si l'usuari existeix i la contrasenya coincideix, iniciem la sessió i informem de que s'ha iniciat la sessió correctament, si no mostrarà un missatge d'error
            if user is not None:
                login(request, user)
                messages.success(request, 'S\'ha iniciat la sessió correctament!')
                return redirect('home')
            else:
                # sino mostrarà un missatge d'error
                messages.error(request, 'No s\'ha pogut iniciar la sessió. Comproveu el email i la contrasenya.')
    else:
        form = UserLoginForm()
    return render(request, 'gym_app/login.html', {'form': form})

# Definim la pàgina d'inici, que es crida quan es visita la url '/'
def home(request):
    return render(request, 'gym_app/home.html')

# Definim la pàgina per tancar la sessió, que es crida quan es visita la url '/logout/'
def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
# Definim la pàgina per editar el perfil de l'usuari, que es crida quan es visita la url '/editar_perfil/'
def editar_perfil(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        # Si el formulari és correcte, actualitzem el perfil de l'usuari i informem de que s'ha actualitzat el perfil correctament, si no mostrarà un missatge d'error
        if form.is_valid():
            form.save()
            messages.success(request, "El perfil s'ha actualitzat correctament!")
            return redirect('editar_perfil')
        else:
            messages.error(request, "No s'ha pogut actualitzar el perfil. Torneu-ho a intentar.")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'gym_app/editar_perfil.html', {'form': form})
        