""" Post model. """

# Django
from django.db import models

# Models
from utilities.models import TimeStamps


class Post(TimeStamps):
    """ Post model.
    Almacena toda la información de una publicación, puede contener imagen
    texto, sentimiento y ubicación.
    """
    # Usuario que publicó el post.
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    # Agregar imagen a un post.
    image_post = models.ImageField(
        blank=True,
        null=True,
        upload_to='posts/pictures')
    # Texto del post.
    text_post = models.TextField()
    # Feeling del post.
    feeling = models.CharField(max_length=50)
    # Ubicación en donde se realizó el post.
    ubication = models.CharField(max_length=100, null=True, blank=True)

    # Reacciones - A través de la tabla ReactionAssignment
    reactions = models.ManyToManyField(
        'posts.Reaction',
        through='posts.ReactionAssignment',
        through_fields=('post', 'reaction')
    )

    # Si el post es privado se mostrará únicamente a los amigos.
    is_private = models.BooleanField(
        'private',
        default=False,
        help_text=('True if user wants the post its private.')
    )
