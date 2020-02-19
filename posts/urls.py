""" Posts urls. """

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Viewsets
from .viewsets import posts as post_views
from .viewsets import comments as comment_views
from .viewsets import reactions as reaction_views

router = DefaultRouter()
# URL's posts
router.register(r'posts', post_views.PostViewSet, basename='posts')
router.register(r'post/(?P<post_id>[0-9]+)/comments', comment_views.PostCommentViewSet, basename='comments')
router.register(r'post/(?P<post_id>[0-9]+)/reactions', reaction_views.PostReactionViewSet , basename='reactions')
# URL's comments
router.register(r'comments', comment_views.CommentViewSet, basename='comments')
# URL's reactions
router.register(r'reactions', reaction_views.ReactionModelViewSet, basename='reactions')

urlpatterns = [
    path('', include(router.urls)),
]