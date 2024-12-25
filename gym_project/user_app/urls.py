from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # Ruta per mostrar el horari de classes
    path('horari_classes/', views.horari_classes, name='horari_classes'),

    # Ruta per desinscriure un usuari d'una classe
    path('desinscriure_me/', views.desinscriure_me, name='desinscriure_me'),

    # Ruta per inscriure un usuari a una classe
    path('inscriure_me/', views.inscriure_me, name='inscriure_me'),

    # Ruta per mostrar la quota d'una classe
    path('quota/', views.quota, name='quota'),

]
