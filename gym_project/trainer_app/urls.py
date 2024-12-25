from django.urls import path
from . import views

app_name = 'trainer'  

urlpatterns = [
    path('crear_rutina/', views.crear_rutina, name='crear_rutina'),
    path('horari/', views.horari, name='horari'),
    path('llistar-rutines/', views.llistar_rutines, name='llistar_rutines'),
    path('previsualitzar/<str:rutina_nom>/', views.previsualitzar, name='previsualitzar'),
    path('editar_rutina/<str:rutina_nom>/', views.editar_rutina, name='editar_rutina'),
    path('eliminar_rutina/<str:rutina_nom>/', views.eliminar_rutina, name='eliminar_rutina'),
    path('asignar_rutina/', views.asignar_rutina, name='asignar_rutina'),
    path('treure_rutina/', views.treure_rutina, name='treure_rutina'),
    
]
