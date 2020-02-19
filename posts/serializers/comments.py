""" Comment Serializer."""

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import serializers

# Models
from posts.models.comments import Comment
from posts.models.posts import Post


class CommentModelSerializer(serializers.ModelSerializer):
    # Permite obtener un campo por medio de la relación, se seleccionó username.
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = (
            'id', 'post', 'text_comment',
             'image_comment', 'user', 'created', 'updated'
        )