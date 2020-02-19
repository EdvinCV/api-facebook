""" Comments model. """

# Django
from django.db import models

# Django REST Framework

# Models
from utilities.models import TimeStamps
from posts.models.posts import Post
from users.models.users import User


class Comment(TimeStamps):
    """ Comment model.
    Permite almacenar información de los comentarios
    a una publicación, almacena el usuario que lo hizo y a que publicación.
    """

    # Post que se comento.
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Usuario que hizo el comentario.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Texto del comentario.
    text_comment = models.TextField()
    # Imagen de comentario
    image_comment = models.ImageField(
        null=True,
        blank=True,
        upload_to='posts/pictures')
