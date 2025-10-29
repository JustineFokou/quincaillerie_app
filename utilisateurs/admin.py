from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ProfilUtilisateur


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'role', 'is_active_employee', 'is_active', 'date_joined'
    ]
    list_filter = ['role', 'is_active_employee', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_editable = ['is_active_employee', 'is_active']
    ordering = ['last_name', 'first_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations professionnelles', {
            'fields': ('role', 'telephone', 'adresse', 'date_embauche', 'salaire', 'is_active_employee')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations professionnelles', {
            'fields': ('role', 'telephone', 'adresse', 'date_embauche', 'salaire', 'is_active_employee')
        }),
    )


@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'theme_preference', 'created_at', 'is_active'
    ]
    list_filter = ['theme_preference', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_editable = ['is_active']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Profil', {
            'fields': ('avatar', 'bio', 'theme_preference')
        }),
        ('Préférences', {
            'fields': ('preferences_notifications',)
        }),
        ('Statut', {
            'fields': ('is_active',)
        })
    )
