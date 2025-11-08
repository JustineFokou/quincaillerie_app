from django.contrib import admin
from .models import CompanySettings


@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    """
    Administration pour les paramètres de l'entreprise
    """
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_entreprise', 'slogan', 'devise')
        }),
        ('Adresse', {
            'fields': ('adresse', 'ville', 'pays')
        }),
        ('Contact', {
            'fields': ('telephone', 'telephone_secondaire', 'email', 'site_web')
        }),
        ('Informations légales', {
            'fields': ('numero_fiscal',)
        }),
        ('Logo', {
            'fields': ('logo',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        """
        Empêche l'ajout de nouvelles instances (singleton)
        """
        return not CompanySettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """
        Empêche la suppression de l'instance (singleton)
        """
        return False
    
    def changelist_view(self, request, extra_context=None):
        """
        Redirige vers la modification au lieu de la liste
        """
        company_settings = CompanySettings.load()
        return super().changeform_view(
            request, 
            str(company_settings.pk), 
            extra_context=extra_context
        )

