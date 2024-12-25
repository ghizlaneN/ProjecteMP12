from djongo import models
from bson import ObjectId 
from gym_app.models import User

# Create your models here.

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
        self.horaris.all().delete()
        super(Rutina, self).delete(*args, **kwargs)
    
#return f"Clase para {self.horari} con {len(self.inscritos)} inscritos"
    
    
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