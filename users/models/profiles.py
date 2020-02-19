""" Profile model. """

# Models
from .users import User
from utilities.models import TimeStamps

# Django
from django.db import models


class Profile(TimeStamps):
    """Profile models
    Información de perfil de un usuario,
    se crea automáticamente al crear un User.
    """
    # Relación con usuario.
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    # Imagen de perfil.
    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures',
        blank=True,
        null=True
    )
    # Imagen de portada.
    cover_photo = models.ImageField(
        'profile cover image',
        upload_to='users/pictures',
        blank=True,
        null=True
    )
    # Biografía.
    biography = models.CharField(max_length=500, blank=True)
    
    # Stats
    number_posts = models.PositiveIntegerField(default=0)
    number_reactions = models.PositiveIntegerField(default=0)

    # Si el perfil es público se muestra toda la información.
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)