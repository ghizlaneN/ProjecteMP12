from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Horari_Classes, Quotes
from trainer_app.models import Horari, Rutina
from datetime import datetime, timedelta
from bson import ObjectId
from .forms import QuotesForm

# Create your views here.
# Definim la vista per a la quota d'usuari
def quota(request):
    if request.method == 'POST':
        # Creem un formulari amb les dades rebudes
        form = QuotesForm(request.POST)
        # Comprovem si el formulari és vàlid
        if form.is_valid():
            # Busquem si ja existeix una quota per aquest usuari
            quota_exist = Quotes.objects.filter(user_id=request.user.id).first()

            # Si la quota existeix, actualitzem la descripció
            if quota_exist:
                quota_exist.quote_description = form.cleaned_data['quote_description']
                quota_exist.save()
                messages.success(request, 'La quota s\'ha actualitzat correctament')
            else:          
                # Si la quota no existeix, la creem
                quota = form.save(commit=False)
                quota.user = request.user
                quota.save()
                messages.success(request, 'Quota guardada correctament.')
            return redirect('user:quota')
        else:
            messages.error(request, 'No s\'ha pogut guardar la quota.')
    else:
        form = QuotesForm(request.POST)
    return render(request, 'quota.html', {'form': form})


# Definim la vista per mostrar l'horari de la classe     
def horari_classes(request):
    # Obtenim totes les classes del model Horari_Classes
    horari_classes = Horari_Classes.objects.all()
    # Obtenim tots els horaris del model Horari
    all_horaris = Horari.objects.all()

    # Inicialitzem un diccionari per guardar les classes de cada dia
    horari = { "Dilluns": {}, "Dimarts": {}, "Dimecres": {}, "Dijous": {}, "Divendres": {} }

    # Processam cada horari per obtenir la informació de la rutina
    for hora in all_horaris:
        key = f"{hora.dia}_{hora.hora}"
        rutina = Rutina.objects.get(rutina_id=ObjectId(hora.rutina_id))        

        # Afegim la informació de la rutina al diccionari horari
        horari[hora.dia][key] = {
            'nom': rutina.nom,
            'hora': hora.hora,
            'id': hora.rutina_id,
            'horari_id': hora.horari_id
        }

    # Generem les hores de 16:00 a 21:00
    hores = [f"{hora}:00" for hora in range(16, 22)]

    # Obtenim les dates de dilluns a divendres de la setmana actual
    avui = datetime.today()  # Data d'avui
    weekday = avui.weekday()  # Dia de la setmana (0=Dilluns, 6=Diumenge)
    principi = avui - timedelta(days=weekday)  # Ajustem per començar des del dilluns

    # Creem un diccionari amb els dies i les seves respectives dates
    dies_setmana = ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres"]
    dates = {}
    for i in range(5):
        dia = dies_setmana[i]

        if i < weekday:
            data = (principi + timedelta(days=i + 7)).strftime("%m/%d")
        else:
            data = (principi + timedelta(days=i)).strftime("%m/%d")

        if weekday == i:
                dia = f"Avui {dia}"
        dates[dia] = data      

    inscrits = {}
    # Comprovem si l'usuari està inscrit a cada classe
    for h_c in horari_classes:
        usuari_inscrit = request.user in h_c.usuari_inscrit.all()

        for dia, rutines in horari.items():
            for key, rutina in rutines.items():
                if str(rutina['horari_id']) == str(h_c.horari_id):
                    inscrits[key] = usuari_inscrit   

    return render(request, 'horari_classes.html', {
        'horari_classes': horari_classes, 
        'horari': horari, 
        'hores': hores, 
        'dates': dates,
        'inscrits': inscrits
    })
    
# Aquesta funció permet a un usuari inscriure's a una classe
def inscriure_me(request):
    if request.method == 'POST':
        # Obtenim l'id del horari del formulari
        horari_id = request.POST.get('horari_id')

        # Comprovem que l'id del horari existeix
        if not horari_id:
            messages.error(request, 'No s\'ha pogut trobar la id del horari.')
            return redirect('user:horari_classes')

        try:
            # Busquem l'horari amb l'id obtinguda
            horari = Horari.objects.get(horari_id=ObjectId(horari_id))
        except Horari.DoesNotExist:
            messages.error(request, 'Horari no trobat')
            return redirect('user:horari_classes')

        try:
            # Busquem la quota de l'usuari actual
            quota_usuari = Quotes.objects.get(user=request.user)
        except Quotes.DoesNotExist:
            messages.error(request, 'No tens una quota disponible')
            return redirect('user:horari_classes')

        # Obtenim el límit de quota de l'usuari
        limit_quota = int(quota_usuari.quote_description[0])
        if limit_quota == 0:
            limit_quota = float('inf')

        # Comprovem el nombre total d'inscripcions de l'usuari
        total_inscripcions = Horari_Classes.objects.filter(
            usuari_inscrit=request.user
        ).count()

        # Comprovem si l'usuari ha superat el límit de quota
        if total_inscripcions >= limit_quota:
            messages.error(request, 'Has superat el límit de inscripcions per setmana')
            return redirect('user:horari_classes')

        try:
            # Busquem la classe amb l'horari obtingut
            horari_classe = Horari_Classes.objects.get(horari=horari)
        except Horari_Classes.DoesNotExist:
            # Si la classe no existeix, la creem automàticament
            horari_classe = Horari_Classes.objects.create(horari=horari)

        # Comprovem si hi ha espai en la classe
        if horari_classe.usuari_inscrit.count() < 10:
            # Si hi ha espai, inscriurem l'usuari a la classe
            horari_classe.usuari_inscrit.add(request.user)
            # Afegim l'usuari a la relació ManyToMany
            messages.success(request, 'S\'ha inscrit correctament.')
        else:
            messages.error(request, 'La classe està plena.')
    return redirect('user:horari_classes')

# Aquesta funció permet a un usuari desinscriure's d'una classe
def desinscriure_me(request):
    if request.method == 'POST':
        # Obtenim l'id del horari del formulari
        horari_id = request.POST.get('horari_id')

        # Comprovem que l'id del horari existeix
        if not horari_id:
            messages.error(request, 'No s\'ha pogut trobar la id del horari.')
            return redirect('user:horari_classes')

        try:
            # Busquem l'horari amb l'id obtinguda
            horari = Horari.objects.get(horari_id=ObjectId(horari_id))
        except Horari.DoesNotExist:
            messages.error(request, 'Horari no trobat')
            return redirect('user:horari_classes')

        try:
            # Busquem la classe amb l'horari obtingut
            horari_classe = Horari_Classes.objects.get(horari=horari)
        except Horari_Classes.DoesNotExist:
            messages.error(request, 'Classe no trobada')
            return redirect('user:horari_classes')

        # Comprovem si l'usuari està inscrit a la classe
        if request.user in horari_classe.usuari_inscrit.all():
            # Si l'usuari està inscrit, el desinscriurem
            horari_classe.usuari_inscrit.remove(request.user)
            messages.success(request, 'S\'ha desinscrit correctament.')
        else:
            messages.error(request, 'No tens aquesta classe inscrita.')
    return redirect('user:horari_classes')