from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserLoginForm, EditProfileForm
from django.contrib.auth.forms import UserChangeForm
from djongo.models import Q
from datetime import datetime, timedelta, time
from bson import ObjectId


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
    user = request.user
    if hasattr(user, 'role'):
        if user.role == 'trainer':
            return redirect('trainer:llistar_rutines')
        elif user.role == 'user':
            return redirect('user:horari_classes')
        elif user.role == 'admin':
            return redirect('admin_app:llistar_usuaris')
        elif user.role == 'director':
            return redirect('gerent_app:llista_usuaris')
    else:
        return redirect('login')

# Definim la pàgina per tancar la sessió, que es crida quan es visita la url '/logout/'
def logout_view(request):
    logout(request)
    return redirect('login')
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
   