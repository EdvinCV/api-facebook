""" Serializers reactions."""

# Django

# Django REST Framework
from rest_framework import serializers

# Models
from posts.models.reaction_assignment import ReactionAssignment


class ReactionAssignmentSerializer(serializers.Serializer):
    """ ReactionAssignment Serializer."""

    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    post = serializers.SlugRelatedField(read_only=True, slug_field='id')
    reaction = serializers.SlugRelatedField(read_only=True, slug_field='short_name')
    class Meta:
        model = ReactionAssignment
        fields = (
            'user',
            'post',
            'reaction',
        )
