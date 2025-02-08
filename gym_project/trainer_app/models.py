from djongo import models
from bson import ObjectId 
from gym_app.models import User

# Crea els teus models aquí

class Rutina(models.Model):
    # Identificador únic de la rutina
    rutina_id = models.ObjectIdField(default=ObjectId)
    # Nom de la rutina
    nom = models.CharField(max_length=100)
    # Breu descripció de la rutina
    descripcio = models.CharField(max_length=100)
    # Detalls dels exercicis de la rutina
    exercicis = models.TextField()
    # Recomanacions addicionals (opcional)
    recomenacions = models.TextField(null=True, blank=True)
    # Entrenador associat a la rutina
    entrenador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rutines')

    class Meta:
        db_table = 'rutines'

    def save(self, *args, **kwargs):
        # Capitalitza el nom abans de guardar
        self.nom = self.nom.capitalize()
        super(Rutina, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nom

    def delete(self, *args, **kwargs):
        # Elimina tots els horaris associats abans d'eliminar la rutina
        self.horaris.all().delete()
        super(Rutina, self).delete(*args, **kwargs)

class Horari(models.Model):
    # Opcions per als dies de la setmana
    dies = [
        ('Dilluns', 'Dilluns'),
        ('Dimarts', 'Dimarts'),
        ('Dimecres', 'Dimecres'),
        ('Dijous', 'Dijous'),
        ('Divendres', 'Divendres'),
    ]
    # Opcions per a les hores disponibles
    horari = [
        ('16:00', '16:00 '),
        ('17:00', '17:00 '),
        ('18:00', '18:00 '),
        ('19:00', '19:00 '),
        ('20:00', '20:00 ')
    ]   

    # Identificador únic de l'horari
    horari_id = models.ObjectIdField(default=ObjectId)
    # Rutina associada a aquest horari
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE , related_name='horaris')
    # Dia de la setmana per a aquest horari
    dia = models.CharField(max_length=10, choices=dies, default="Dilluns")
    # Hora del dia per a aquest horari
    hora = models.CharField(max_length=5, choices=horari, default="16:00")

    class Meta:
        db_table = 'horaris'

    def __str__(self):
        return f'{self.dia} {self.hora}'