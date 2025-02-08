from django.shortcuts import render, get_object_or_404, redirect
from gym_app.models import User
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.


def llista_usuaris(request):
    usuaris = User.objects.all()
    
    cerca = request.GET.get('c','')
    usuaris = User.objects.filter(
        Q(first_name__icontains=cerca) |
        Q(last_name__icontains=cerca) |
        Q(email__icontains=cerca) |
        Q(username__icontains=cerca)
    )
    
    ordenar = request.GET.get('ordenar', 'id')
    usuaris = usuaris.order_by(ordenar)
    
    paginacio = Paginator(usuaris, 10)
    num_pag = request.GET.get('pagina')
    pag_obj = paginacio.get_page(num_pag)
    return render(request, 'llista_usuaris.html', {'pag_obj': pag_obj, 'ordenar': ordenar})