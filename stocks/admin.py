from django.contrib import admin
from .models import MouvementStock


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = [
        'produit', 'type_mouvement', 'quantite', 'motif', 
        'reference', 'prix_unitaire', 'valeur_totale', 'date_mouvement', 'is_active'
    ]
    list_filter = ['type_mouvement', 'motif', 'is_active', 'date_mouvement']
    search_fields = ['produit__nom', 'produit__code_produit', 'reference', 'commentaire']
    list_editable = ['is_active']
    ordering = ['-date_mouvement']
    readonly_fields = ['valeur_totale']
    
    fieldsets = (
        ('Mouvement', {
            'fields': ('produit', 'type_mouvement', 'quantite', 'motif')
        }),
        ('Informations', {
            'fields': ('reference', 'prix_unitaire', 'valeur_totale', 'date_mouvement')
        }),
        ('Acteurs', {
            'fields': ('fournisseur', 'client')
        }),
        ('Commentaire', {
            'fields': ('commentaire',)
        }),
        ('Statut', {
            'fields': ('is_active',)
        })
    )
