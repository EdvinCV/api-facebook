""" Users urls. """

from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .viewsets import users as user_views

router = DefaultRouter()
# URL's user.
router.register('users', user_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]