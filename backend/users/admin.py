from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'prenom', 'nom', 'role', 'is_active', 'is_banned', 'created_at']
    list_filter = ['role', 'is_active', 'is_banned']
    search_fields = ['email', 'prenom', 'nom']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('prenom', 'nom', 'whatsapp', 'facebook', 'instagram', 'photo_profil')}),
        ('Rôle et statut', {'fields': ('role', 'is_active', 'is_banned', 'email_verified')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'prenom', 'nom', 'whatsapp', 'password1', 'password2'),
        }),
    )