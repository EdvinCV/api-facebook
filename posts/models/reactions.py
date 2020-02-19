""" Reaction model. """

# Django
from django.db import models

# Models
from utilities.models import TimeStamps

class Reaction(TimeStamps):
    """ Reaction model.
    Tipo de reacción que se le puede asignar a una publicación,
    permite manejar número variable de reacciones.
    """

    # Descripción corta de la reacción.
    short_name = models.CharField(max_length=50)
    # Imagen que identifica a la reacción.
    image_reaction = models.ImageField(upload_to='reactions/pictures' , blank=True, null=True)
