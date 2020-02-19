""" Django Users Models. """

# Models
from utilities.models import TimeStamps
from django.contrib.auth.models import AbstractUser

# Django
from django.db import models


class User(TimeStamps, AbstractUser):
    """Custom user model
    Extends from AbstractUser model from Django, change the username field to email
    and add extra fields.
    """

    # Cambiar el campo por defecto de autenticación.
    USERNAME_FIELD= 'email'
    # Campos requeridos al crear un usuario.
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'gender']

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    MALE = 0
    FEMALE = 1
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    # Género de la persona.
    gender = models.IntegerField(choices=GENDER_CHOICES)

    # Número de teléfono.
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Verificación de email.
    is_verified = models.BooleanField(
        'verified', 
        default=False, 
        help_text=('Set to true when the user have verified its email.')
    )
    