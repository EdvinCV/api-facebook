""" Profile serializers."""

# Django

# Django REST Framework
from rest_framework import serializers

# Models
from users.models.profiles import Profile
from posts.models.comments import Comment
from posts.models.posts import Post
from posts.models.reaction_assignment import ReactionAssignment

class ProfileModelSerializer(serializers.ModelSerializer):
    """ Profile serializer.
    Muestra todos los campos de perfil, adicional calcula el 
    numero de post total, el total de comentarios por todos los post
    y el total de reacciones por todos los post.
    """

    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    # Número total de post del usuario.
    number_posts = serializers.SerializerMethodField('get_total_posts')
    # Número total de comentarios de todos los post.
    total_comments_of_posts = serializers.SerializerMethodField('get_total_stats')
    # Número total de reacciones de todos los post.
    total_reactions_of_posts = serializers.SerializerMethodField('get_total_stats_reactions')

    class Meta:
        model = Profile
        fields = (
            'user',
            'picture',
            'cover_photo',
            'biography',
            'number_posts',
            'number_reactions',
            'total_comments_of_posts',
            'total_reactions_of_posts',
        )

    # Funcion para obtener total post.
    def get_total_posts(self, obj):
        return Post.objects.filter(user=obj.user).count()

    # Funcion para obtener total de comentarios
    def get_total_stats(self, obj):
        posts = Post.objects.filter(user=obj.user)
        total_comments = 0
        for post in posts:
            total_comments += Comment.objects.filter(post=post).count()
        return total_comments

    # Funcion para obtener total de reacciones.
    def get_total_stats_reactions(self, obj):
        posts = Post.objects.filter(user=obj.user)
        total_reactions = 0
        for post in posts:
            total_reactions += ReactionAssignment.objects.filter(post=post).count()
        return total_reactions

