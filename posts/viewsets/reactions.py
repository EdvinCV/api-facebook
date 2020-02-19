""" Reactions viewset. 
    Este viewset solo puede ser utilizado por un usuario administrador
    para editar las reacciones disponibles.
"""

# Models
from posts.models.reactions import Reaction
from posts.models.posts import Post
from posts.models.reaction_assignment import ReactionAssignment

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
# Serializers
from posts.serializers.reactions import ReactionAssignmentSerializer


class ReactionModelViewSet(viewsets.ModelViewSet):
    """ ReactionModelViewSet. 
    Permite asignar una reacción a una publicación.
    """
    serializer_class = ReactionAssignmentSerializer

    class Meta:
        model = Reaction
        fields = (
            'short_name',
            'image_reaction'
        ) 

    # Acción que permite asignar una reacción a una publicación.
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def asign(self, request, *args, **kwargs):
        # Inicializar reacción encontrada.
        reaction_founded = []
        # Obtener post.
        post = get_object_or_404(Post, pk=request.data['post_id'])
        # Obtener reacción.
        reaction = get_object_or_404(Reaction, pk=request.data['reaction_id'])
        # Obtener usuario autenticado.
        user = self.request.user
        # Busca que exista una reaccion del usuario en el post.
        try:
            # Si encuentra lo asigna a la variable.
            reaction_founded = ReactionAssignment.objects.get(post=post, user=user)
        except ReactionAssignment.DoesNotExist:
            # Si no encuentra deja la variable vacía.
            reaction_founded = []
        
        if not reaction_founded:
            # Si no existe reacción al post, crea una nueva
            new_reaction = ReactionAssignment.objects.create(post=post, user=user, reaction=reaction)
            new_reaction.save()
        elif reaction_founded:
            # Si reacción encontrada es del mismo tipo a reacción enviada, elimina la reacción.
            if reaction == reaction_founded.reaction:
                ReactionAssignment.objects.filter(reaction=reaction, user=user).delete()
            # Si reacción encontrada es de diferente tipo, actualiza el tipo.
            else:
                reaction_founded.reaction = reaction
                reaction_founded.save()
        return Response(status=status.HTTP_200_OK)


class PostReactionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """PostReactionViewSet
    Permite obtener todas las reacciones de
    un post a través del post_id que se de al
    endpoint.
    """

    serializer_class = ReactionAssignmentSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verificar que el post exista."""
        post_id = kwargs['post_id']
        # Permite obtener el post con el que se esta trabajando.
        self.post = get_object_or_404(Post, pk=post_id)
        return super(PostReactionViewSet, self).dispatch(request, *args, **kwargs)

    # Obtiene todas las reacciones del post encontrado.
    def get_queryset(self):
        """Retorna las reacciones de una publicación."""
        return ReactionAssignment.objects.filter(
            post=self.post.id
        )
