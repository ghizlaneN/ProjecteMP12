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
    
class Rutina(models.Model):
    rutina_id = models.ObjectIdField(default=ObjectId)
    nom = models.CharField(max_length=100)
    descripcio = models.CharField(max_length=100)
    exercicis = models.TextField()
    recomenacions = models.TextField(null=True, blank=True)
    entrenador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rutines')

    class Meta:
        db_table = 'rutines'
    
    def save(self, *args, **kwargs):
        self.nom = self.nom.capitalize()
        super(Rutina, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.nom
    
    def delete(self, *args, **kwargs):
        # Eliminar manualmente los horarios asociados a esta rutina
        self.horaris.all().delete()  # Esto elimina todos los horarios relacionados
        super(Rutina, self).delete(*args, **kwargs)
    
class Horari(models.Model):
    dies = [
        ('Dilluns', 'Dilluns'),
        ('Dimarts', 'Dimarts'),
        ('Dimecres', 'Dimecres'),
        ('Dijous', 'Dijous'),
        ('Divendres', 'Divendres'),
    ]
    horari = [
        ('16:00', '16:00 '),
        ('17:00', '17:00 '),
        ('18:00', '18:00 '),
        ('19:00', '19:00 '),
        ('20:00', '20:00 ')
    ]   
    
    horari_id = models.ObjectIdField(default=ObjectId)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE , related_name='horaris')
    dia = models.CharField(max_length=10, choices=dies, default="Dilluns")
    hora = models.CharField(max_length=5, choices=horari, default="16:00")
    
    class Meta:
        db_table = 'horaris'
        
    def __str__(self):
        return f'{self.dia} {self.hora}'
    
    @staticmethod
    def get_item(horario_dict, dia, hora):
        try:
            key = f"{dia}_{hora}"
            return horario_dict.get(dia, {}).get(key, None)
        except KeyError:
            return None