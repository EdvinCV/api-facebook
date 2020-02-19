from django.contrib import admin

#Models
from posts.models.posts import Post
from posts.models.comments import Comment
from posts.models.reactions import Reaction
from posts.models.reaction_assignment import ReactionAssignment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('text_post',)

@admin.register(Comment)
class ComentAdmin(admin.ModelAdmin):
    list_display = ('text_comment',)

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('short_name',)

@admin.register(ReactionAssignment)
class ReactionAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'reaction')