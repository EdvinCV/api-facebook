""" User viewsets """

# Models
from users.models import User

# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# Permissions
from users.permissions.users import IsAccountOwner

#Serializers
from users.serializers.users import (
    UserSignupSerializer, 
    UserModelSerializer, 
    AccountVerificationSerializer, 
    UserLoginSerializer,
)
from users.serializers.profiles import (
    ProfileModelSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """UserViewSet
    Acciones de usuario.
    """

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Asignar permisos según la acción."""
        permissions = []
        if self.action in ['update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        if self.action == 'list':
            permissions.append(IsAuthenticated)
        if self.action == 'create':
            permissions.append(IsAuthenticated)
        return [p() for p in permissions]

    # Acción para el signup.
    @action(detail=False, methods=['post'])
    def signup(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Regresar información de usuario.
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    # Acción para la verificación de cuenta.
    @action(detail=False, methods=['post'])
    def verify(self, request, *args, **kwargs):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulations. You have activate your account.'
        }
        # Regresa mensaje de data.
        return Response(data, status=status.HTTP_200_OK)

    # Acción para actualizar información de perfil.
    @action(detail=True, methods=['put', 'patch'], permission_classes=[IsAuthenticated, IsAccountOwner])
    def profile(self, request, *args, **kwargs):
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)     

    # Acción para el login del usuario.
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        # Regresa información del usuario logueado y su access_token
        return Response(data, status=status.HTTP_201_CREATED)