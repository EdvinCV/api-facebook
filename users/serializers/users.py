""" User serializers. """

# Django
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.mail import EmailMultiAlternatives

# Djando REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from users.models import User, Profile

# Render to string
from django.template.loader import render_to_string

# Utilities
import jwt
from datetime import timedelta

# Serializers
from users.serializers.profiles import ProfileModelSerializer


class UserModelSerializer(serializers.ModelSerializer):

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'profile'
        )

class UserSignupSerializer(serializers.Serializer):
    """User Signup serializer
    Obtiene todas las validaciones para el signup.
    """

    # Campos para validar.
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password =  serializers.CharField(max_length=24, min_length=8)
    password_confirmation = serializers.CharField(max_length=24, min_length=8)
    
    phone_regex = RegexValidator(
        regex=r'\+1?\d{9,15}$',
        message="Phone number must be entered in the format."
    )
    phone = serializers.CharField(validators=[phone_regex], required=False)

    MALE = 0
    FEMALE = 1
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)

    def validate(self, data):
        """Verificar que las contraseñas enviadas coincidan. """
        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            # Si las contraseñas no son iguales, envía error.
            raise serializers.ValidationError(" Passwords doesn't match.")
        # Verificar si la contraseña cumple con las reglas.
        password_validation.validate_password(password)
        return data
    
    def create(self, data):
        data.pop('password_confirmation')
        # Crear usuario, por defecto no esta verificado.
        user = User.objects.create_user(**data, is_verified=False)
        # Crea perfil con usuario recién creado.
        profile = Profile.objects.create(user=user, is_public=True)
        # Enviar correo de confirmación.
        self.send_confirmation_email(user)
        return user
    
    def send_confirmation_email(self, user):
        # Generar token para verificación.
        verification_token = self.generate_token(user)
        # Asunto del email
        subject = '{}, Welcome to Facebook! Please, verify your account to start meeting people.'.format(user.username)
        # Destinatario
        from_email = 'Facebook admin@facebook.com'
        # Contenido del correo, template.
        content = render_to_string('emails/users/account_verification.html', {'token': verification_token, 'user':user})
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()
        
    def generate_token(self, user):
        """Crear JWT para verificar cuenta de usuario."""
        exp_date = timezone.now() + timedelta(days=5)
        payload = {
            'user': user.username,
            'email': user.email,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY , algorithm='HS256')
        return token.decode()

class AccountVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, data):
        """Verificar que el token sea válido. """
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
        self.context['payload'] = payload
        return data

    def save(self):
        """ Actualiza estado de verificado de usuario. """
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """ Verifica que exista usuario con las credenciales enviadas. """
        user = authenticate(username=data['email'], password=data['password'])
        # Si no existe usuario envía error.
        if not user: 
            raise serializers.ValidationError('Invalid credentials.')
        # Si existe pero no esta verificado envía error.
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet.')
        # Almacena el usuario en el contexto.
        self.context['user'] = user
        return data
    
    def create(self, data):
        """ Cuando se crea un usuario se crea un Token. """
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
