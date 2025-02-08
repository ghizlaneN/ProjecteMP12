from django.urls import path
from . import views

app_name = 'gerent_app'

urlpatterns = [
    path('llista_usuaris/', views.llista_usuaris, name='llista_usuaris'),
]
