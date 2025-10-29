from django.contrib import admin
from .models import Fournisseur


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = [
        'nom', 'contact', 'email', 'telephone', 'ville', 
        'delai_livraison', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'pays', 'created_at']
    search_fields = ['nom', 'contact', 'email', 'ville']
    list_editable = ['is_active']
    ordering = ['nom']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'contact', 'email', 'telephone')
        }),
        ('Adresse', {
            'fields': ('adresse', 'ville', 'code_postal', 'pays')
        }),
        ('Informations commerciales', {
            'fields': ('numero_tva', 'conditions_paiement', 'delai_livraison')
        }),
        ('Notes', {
            'fields': ('note',)
        }),
        ('Statut', {
            'fields': ('is_active',)
        })
    )
