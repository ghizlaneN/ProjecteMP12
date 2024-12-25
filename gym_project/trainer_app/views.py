from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CrearRutinaForm, EditRutinaForm
from .models import Rutina, Horari
from bson import ObjectId
import uuid




# Create your views here.
@login_required      
def crear_rutina(request):
    if request.method == 'POST':
        form = CrearRutinaForm(request.POST)
        if form.is_valid():
        
            nom = form.cleaned_data['nom'].capitalize()
            
            if Rutina.objects.filter(nom=nom).count() > 0:
                messages.error(request, "Ja existeix una rutina amb aquest nom.")
                return render(request, 'gym_app/crear_rutina.html', {'form': form})

            rutina = form.save(commit=False)
            rutina.entrenador = request.user 
            rutina.save()
            
            messages.success(request, "La rutina s'ha creat correctament!")
            return redirect('trainer:llistar_rutines')

        else:
            messages.error(request, "No s'ha pogut crear la rutina. Torneu-ho a intentar.")
    else:
        form = CrearRutinaForm()
    return render(request, 'gym_app/crear_rutina.html', {'form': form})

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
    return render(request, 'gym_app/horari.html', {
        'horari': horari, 
        'hores': hores, 
        'all_rutines':all_rutines})
    
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
            return redirect('trainer:llistar_rutines')
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
        return redirect('trainer:llistar_rutines')
    return render(request, 'gym_app/eliminar_rutina.html', {'rutina': rutina})   

def asignar_rutina(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        rutina_id = request.POST.get('rutina_id')
                
        if key and rutina_id:
            dia, hora = key.split('_')
            
            try:
                horari, created = Horari.objects.get_or_create(
                    dia=dia, 
                    hora=hora,
                    defaults={'rutina_id': rutina_id}
                )
                
                if not created:
                    horari.rutina_id = rutina_id
                    horari.save()
                
                messages.success(request, 'Rutina asignada correctament')
            
            except Exception as e:
                messages.error(request, f'Error al asignar rutina {str(e)}')
    return redirect('trainer:horari')

def treure_rutina(request):
    if request.method == 'POST':
        horari_id = request.POST.get('horari_id')        
        horari = Horari.objects.get(horari_id=ObjectId(horari_id))
        horari.delete()
        messages.success(request, 'Rutina treta correctament')
        return redirect('trainer:horari')
    return render(request, 'gym/horari.html', {'horari': horari})