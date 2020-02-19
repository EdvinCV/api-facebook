""" Reaction asignment model. """

# Django
from django.db import models

# Models
from utilities.models import TimeStamps


class ReactionAssignment(TimeStamps):
    """ ReactionAssignment model
    Asignación de un tipo reacción a una publicación.
    """
    # Usuario que reacciono a la publicación.
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    # Tipo de reacción que se asigno.
    reaction = models.ForeignKey('posts.Reaction', on_delete=models.CASCADE)
    # Post al que se reaccionó.
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
