""" Posts serializers. """

# Django REST Framework
from rest_framework import serializers

# Model
from posts.models.posts import Post
from posts.models.comments import Comment
from posts.models.reaction_assignment import ReactionAssignment

# Serializers
from posts.serializers.comments import CommentModelSerializer


class PostModelSerializer(serializers.ModelSerializer):
    # Permite obtener un campo por medio de la relación, se seleccionó username.
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    # Obtener comentarios a través de un serializer.
    comments = CommentModelSerializer(read_only=True, many=True)
    # Obtener total comentarios por publicación, a traves de get_total_comments.
    total_comments = serializers.SerializerMethodField('get_total_comments')
    # Obtener total reacciones por publicación, a traves de get_total_reactions.
    total_reactions = serializers.SerializerMethodField('get_total_reactions')

    class Meta:
        model = Post
        
        fields = (
            'id','image_post',
            'text_post', 'feeling', 'user',
            'ubication', 'comments', 'total_comments', 'total_reactions'
        )

    # Obtener total comentarios.
    def get_total_comments(self, obj):
        return Comment.objects.filter(post=obj.id).count()

    # Obtener total reacciones.
    def get_total_reactions(self, obj):
        return ReactionAssignment.objects.filter(post=obj.id).count()

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'text_comment',
        )