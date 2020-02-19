""" Comment viewset. """

# Django

# Django REST framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import mixins

# Models
from posts.models.comments import Comment
from posts.models.posts import Post

# Serializers
from posts.serializers.comments import CommentModelSerializer

# Permissions
from users.permissions.users import IsCommentOwner


class CommentViewSet(viewsets.ModelViewSet):
    """CommentViewSet
    Permite realizar todas las acciones de ModelViewSet
    sobre comentarios.
    """

    # Obtiene todos los comentarios independientemente del post.
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        """ Asignación de permisos según la acción a realizar. """
        permissions = []
        if self.action == 'list':
            permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'delete', 'destroy']:
            permissions = [IsAuthenticated, IsCommentOwner]
        return (p() for p in permissions)

    # Al momento de crear, se envía el usuario que realizó el comentario.
    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)


class PostCommentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """PostCommentViewSet
    Permite obtener todos los comentarios de
    un post a través del post_id que se de al
    endpoint.
    """

    serializer_class = CommentModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verificar que el post exista."""
        post_id = kwargs['post_id']
        # Permite obtener el post con el que se esta trabajando.
        self.post = get_object_or_404(Post, pk=post_id)
        return super(PostCommentViewSet, self).dispatch(request, *args, **kwargs)

    # Obtiene todos los comentarios del post encontrado.
    def get_queryset(self):
        """Retorna los commentarios de una publicación."""
        return Comment.objects.filter(
            post=self.post.id
        )