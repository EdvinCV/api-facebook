""" Posts ViewSets """

# Django

# Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.response import Response

# Models
from posts.models.posts import Post
from posts.models.comments import Comment

# Serializers
from posts.serializers.posts import PostModelSerializer, PostCommentSerializer
from posts.serializers.comments import CommentModelSerializer

# Permissions
from users.permissions.users import IsAccountOwner, IsPostOwner


class PostViewSet(viewsets.ModelViewSet):
    """PostViewSet. """
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        """Asignar permisos en base a la acción a realizar."""
        permissions = []
        if self.action == 'list':
            permissions = [IsAuthenticated]
        if self.action == 'create':
            permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsPostOwner]
        return [p() for p in permissions]

    def get_queryset(self):
        """Si la acción es listar muestra solo los post públicos"""
        queryset = Post.objects.all()
        if self.action == 'list':
            return queryset.filter(is_private=False)
        return queryset

    # Al crear un nuevo post, obtiene el usuario autenticado.
    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
