from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

# Definim les rutes de l'aplicació
urlpatterns = [
    # Ruta per la pàgina d'inici, apunta a la funció 'home' del fitxer 'views.py'
    path('', views.home, name='home'),
    # Ruta per registrar un nou usuari, apunta a la funció 'register' del fitxer 'views.py'
    path('register/', views.register, name='register'),
    # Ruta per iniciar sessió, apunta a la funció 'user_login' del fitxer 'views.py'
    path('login/', views.user_login, name='login'),
    # Ruta per editar el perfil de l'usuari, apunta a la funció 'editar_perfil' del fitxer 'views.py'
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    # Ruta per tancar sessió, apunta a la vista LogoutView de Django amb la pàgina de destí 'home'
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # Ruta per l'administració de Django, apunta a la url de l'administrador
    path('admin/', admin.site.urls),
    # path('crear_rutina/', views.crear_rutina, name='crear_rutina'),
    # path('horari/', views.horari, name='horari'),
    # path('llistar-rutines/', views.llistar_rutines, name='llistar_rutines'),
    # path('previsualitzar/<str:rutina_nom>/', views.previsualitzar, name='previsualitzar'),
    # path('editar_rutina/<str:rutina_nom>/', views.editar_rutina, name='editar_rutina'),
    # path('eliminar_rutina/<str:rutina_nom>/', views.eliminar_rutina, name='eliminar_rutina'),
    # path('asignar_rutina/', views.asignar_rutina, name='asignar_rutina'),
    # path('treure_rutina/', views.treure_rutina, name='treure_rutina'),
    
]