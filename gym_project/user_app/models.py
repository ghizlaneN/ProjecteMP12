from trainer_app.models import Horari
from gym_app.models import User
from djongo import models
from bson import ObjectId 


class Quotes(models.Model):
    # Opcions de quotes disponibles
    descripcio = [
        ('1', '1 rutina a la setmana amb un preu de 15€ al mes'),
        ('3', '3 rutines a la setmana amb un preu de 30€ al mes'),
        ('0', 'Rutines ilimitades amb un preu de 50€ al mes')   
    ]

    # Identificador únic de la quota
    quote_id = models.ObjectIdField(default=ObjectId)
    # Relació amb l'usuari que té la quota
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='quotes', null=False)
    # Descripció de la quota seleccionada
    quote_description = models.CharField(max_length=100, choices=descripcio, default='1')

    class Meta:
        # Nom de la taula a la base de dades
        db_table = 'quotes'

    def __str__(self):
        # Representació en string de la quota
        return f'{self.user_id} - {self.quote_description}'

class Horari_Classes(models.Model):
    # Identificador únic de la classe
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    # Relació amb l'horari de la classe
    horari = models.ForeignKey(Horari, on_delete=models.CASCADE, related_name='horari_classes')
    # Relació molts a molts amb els usuaris inscrits a la classe
    usuari_inscrit = models.ManyToManyField(
        User, related_name='usuari_inscrit'
    )

    class Meta:
        # Nom de la taula a la base de dades
        db_table = 'horari_classes'

    def __str__(self):
        # Llista d'IDs dels usuaris inscrits
        usuaris = [user.id for user in self.usuari_inscrit.all()]
        return f'Clase ID: {self._id}, Horario: {self.horari}, {usuaris}'
