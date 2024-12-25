from trainer_app.models import Horari
from gym_app.models import User
from djongo import models
from bson import ObjectId 

class Quotes(models.Model):
    descripcio = [
        ('1', '1 rutina a la setmana amb un preu de 15€ al mes'),
        ('3', '3 rutines a la setmana amb un preu de 30€ al mes'),
        ('0', 'Rutines ilimitades amb un preu de 50€ al mes')   
    ]

    quote_id = models.ObjectIdField(default=ObjectId)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='quotes', null=False)
    quote_description = models.CharField(max_length=100, choices=descripcio, default='1')

    class Meta:
        db_table = 'quotes'

    def __str__(self):
        return f'{self.user_id} - {self.quote_description}'

# Create your models here.
class Horari_Classes(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    horari = models.ForeignKey(Horari, on_delete=models.CASCADE, related_name='horari_classes')
    usuari_inscrit = models.ManyToManyField(
        User, related_name='usuari_inscrit'
    )

    class Meta:
        db_table = 'horari_classes'


    def __str__(self):
        usuaris = [user.id for user in self.usuari_inscrit.all()]
        return f'Clase ID: {self._id}, Horario: {self.horari}, {usuaris}'
