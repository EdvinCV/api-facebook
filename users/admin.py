""" User models admin. """

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from users.models import User, Profile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    """User model admin"""

    list_display = ('email','username','first_name','last_name','is_staff','is_verified')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'biography')
    search_fields = ('user__email',)


admin.site.register(User, CustomUserAdmin)