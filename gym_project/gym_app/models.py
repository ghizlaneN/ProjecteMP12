from django.contrib.auth.models import AbstractUser
from djongo import models
from bson import ObjectId 

class User(AbstractUser):
    # Creem una nova columna per el rol del usuari (admin, user, trainer, director)
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('user', 'Usuari del Gimnàs'),
        ('trainer', 'Entrenador'),
        ('director', 'Director')
    ]
    # Camp per l'adreça electrònica, ha de ser única per cada usuari
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    # Canviem el camp que s'utilitza per iniciar sessió a l'email
    USERNAME_FIELD = 'email'
    # Camps obligatoris quan es creï un nou usuari
    REQUIRED_FIELDS = ['username', 'role'] 

    # Canviem el nom de la taula a 'users'
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"  