""" User custom permissions. """

# Django REST Framework
from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
    """Permite al usuario actualizar su perfil. """
    def has_object_permission(self, request, view, obj):
        return request.user == obj

class IsPostOwner(BasePermission):
    """ Permite editar/eliminar el post si es propietario. """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

class IsCommentOwner(BasePermission):
    """ Permite editar/eliminar el comentario si es propietario. """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user