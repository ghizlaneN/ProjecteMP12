from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm, CrearRutinaForm, EditRutinaForm
from django.contrib.auth.forms import UserChangeForm
from .models import Rutina, Horari
from djongo.models import Q
from datetime import datetime, timedelta, time
from bson import ObjectId


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
        
@login_required      
def crear_rutina(request):
    if request.method == 'POST':
        form = CrearRutinaForm(request.POST)
        if form.is_valid():
        
            nom = form.cleaned_data['nom'].capitalize()
            
            if Rutina.objects.filter(nom=nom).exists():
                messages.error(request, "Ja existeix una rutina amb aquest nom.")
                return render(request, 'gym_app/crear_rutina.html', {'form': form})

            # Crear la rutina sin necesidad de especificar el horario
            rutina = form.save(commit=False)
            rutina.entrenador = request.user 
            rutina.save()
            
            messages.success(request, "La rutina s'ha creat correctament!")
            return redirect('llistar_rutines')
        else:
            messages.error(request, "No s'ha pogut crear la rutina. Torneu-ho a intentar.")
    else:
        form = CrearRutinaForm()
    return render(request, 'gym_app/crear_rutina.html', {'form': form})

# nombre unique 
@login_required
def horari(request):

    all_rutines = Rutina.objects.all()    
    all_horaris = Horari.objects.all()
    horari = { "Dilluns": {}, "Dimarts": {}, "Dimecres": {}, "Dijous": {}, "Divendres": {} }
    
    for hora in all_horaris:
        key = f"{hora.dia}_{hora.hora}"
        rutina = Rutina.objects.get(rutina_id=ObjectId(hora.rutina_id))
        
        horari[hora.dia][key] = {
            'nom': rutina.nom,
            'hora': hora.hora,
            'id': rutina.rutina_id,
            'horari_id': hora.horari_id
        }
            # horari[horari.dia].append(horari_info)
    hores = [f"{hora}:00" for hora in range(16,22)]
    return render(request, 'gym_app/horari.html', {'horari': horari, 'hores': hores, 'all_rutines':all_rutines})

def llistar_rutines(request):
    rutines = Rutina.objects.all()
    llista_rutines = list(rutines)
    return render(request, 'gym_app/llistar_rutines.html', {'llista_rutines': llista_rutines})   
    
def previsualitzar(request, rutina_nom):
    rutina = Rutina.objects.filter(nom=rutina_nom).first()
    return render(request, 'gym_app/previsualitzar.html', {'rutina': rutina})

def editar_rutina(request,rutina_nom):
    rutina = Rutina.objects.filter(nom=rutina_nom).first()
    if request.method == 'POST':
        form = EditRutinaForm(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            messages.success(request, "La rutina s'ha editat correctament!")
            return redirect('llistar_rutines')
        else:
            messages.error(request, "No s'ha pogut editar la rutina. Torneu-ho a intentar.")
    else:
        form = EditRutinaForm(instance=rutina)
    return render(request, 'gym_app/editar_rutina.html', {'form': form})

def eliminar_rutina(request,rutina_nom = None):
    rutina = get_object_or_404(Rutina, nom=rutina_nom)
    
    if request.method == 'POST':
        rutina = get_object_or_404(Rutina, nom = rutina_nom)
        rutina.delete()
        messages.success(request, "La rutina s'ha eliminat correctament!")
        return redirect('llistar_rutines')
    return render(request, 'gym_app/eliminar_rutina.html', {'rutina': rutina})   

def asignar_rutina(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        rutina_id = request.POST.get('rutina_id')
                
        if key and rutina_id:
            dia, hora = key.split('_')
            
            try:
                # Intenta obtener el Horari existente
                horari, created = Horari.objects.get_or_create(
                    dia=dia, 
                    hora=hora,
                    defaults={'rutina_id': rutina_id}
                )
                
                # Si no fue creado, actualiza la rutina
                if not created:
                    horari.rutina_id = rutina_id
                    horari.save()
                
                messages.success(request, 'Rutina asignada correctament')
            
            except Exception as e:
                messages.error(request, f'Error al asignar rutina: {str(e)}')
    return redirect('horari')

def treure_rutina(request):
    if request.method == 'POST':
        horari_id = request.POST.get('horari_id')        
        horari = Horari.objects.get(horari_id=ObjectId(horari_id))
        horari.delete()
        messages.success(request, 'Rutina treta correctament')
        return redirect('horari')
    return render(request, 'gym/horari.html', {'horari': horari})