from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    path('llistar_usuaris/', views.llistar_usuaris, name='llistar_usuaris'),
    
    path('editar_usuari/<str:usuari_id>/', views.editar_usuari, name='editar_usuari'),
    path("eliminar_usuari/<str:usuari_id>/", views.eliminar_usuari, name="eliminar_usuari"),
    path("previsualitzar_usuari/<str:usuari_id>/", views.previsualitzar_usuari, name="previsualitzar_usuari"),
    path('crear_usuari/', views.crear_usuari, name='crear_usuari')

]
