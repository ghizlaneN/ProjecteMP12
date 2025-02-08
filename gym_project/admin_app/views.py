from django.shortcuts import render, get_object_or_404, redirect
from gym_app.models import User
from user_app.models import Quotes

from django.contrib import messages
from .forms import UserRegistrationForm, EditUserForm
from django.core.paginator import Paginator


# Create your views here.

# Llistem els usuaris
def llistar_usuaris(request):
    usuaris = User.objects.all()
    paginacio = Paginator(usuaris, 10)
    num_pag = request.GET.get('pagina')
    pag_obj = paginacio.get_page(num_pag)
    return render(request, 'llistar_usuaris.html', {'pag_obj': pag_obj})

def eliminar_usuari(request, usuari_id):
    usuari = get_object_or_404(User, id=usuari_id)
    if request.method == 'POST':
        usuari = get_object_or_404(User, id=usuari_id)
        usuari.delete()
        messages.success(request, "El usuari s'ha eliminat correctament")
        return redirect('admin_app:llistar_usuaris')
    return render(request, 'eliminar_usuari.html', {'usuari': usuari})

def editar_usuari(request,usuari_id):
    usuari = get_object_or_404(User, id=usuari_id)
    quote = Quotes.objects.filter(user_id=usuari_id).first()
    initial_quote = Quotes.quote_description if quote else None
    user_role = usuari.role

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=usuari, user_role=user_role)
        if form.is_valid():
            form.save()
            quote_description = form.cleaned_data['quote_description']
            if user_role == 'user':
                if quote:
                    quote.quote_description = quote_description
                    quote.save()
                else:
                    Quotes.objects.create(user=usuari, quote_description=quote_description)

            messages.success(request, "El usuari s'ha editat correctament")
            return redirect('admin_app:llistar_usuaris')
        else:
            messages.error(request, "No s'ha pogut editar l'usuari")
    else:
        form = EditUserForm(instance=usuari, user_role=user_role, initial_quote=initial_quote)
    return render(request, 'editar_usuari.html', {'form': form})

def previsualitzar_usuari(request,usuari_id):
    usuari = User.objects.filter(id=usuari_id).first()
    return render(request, 'previsualitzar_usuari.html', {'usuari':usuari})

def crear_usuari(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # Si el formulari és correcte, registrem l'usuari i iniciem la sessió sino mostrarà un missatge d'error
        if form.is_valid():
            form.save()
            messages.success(request, "El registre s'ha completat correctament!")
            return redirect('admin_app:llistar_usuaris')
        else:
            messages.error(request, "No s'ha pogut completar el registre. Torneu-ho a intentar.")
    else:
        # Si no es POST, creem un nou formulari per registrar-se
        form = UserRegistrationForm()
    return render(request, 'crear_usuari.html', {'form': form})
