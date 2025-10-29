from django.contrib import admin
from .models import Vente, LigneVente


class LigneVenteInline(admin.TabularInline):
    model = LigneVente
    extra = 0
    readonly_fields = ['montant_ligne']
    fields = ['produit', 'quantite', 'prix_unitaire', 'montant_ligne']


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = [
        'numero_vente', 'client_nom', 'statut', 'montant_total', 
        'montant_final', 'mode_paiement', 'date_vente', 'is_active'
    ]
    list_filter = ['statut', 'mode_paiement', 'is_active', 'date_vente']
    search_fields = ['numero_vente', 'client_nom', 'client_email']
    list_editable = ['statut', 'is_active']
    ordering = ['-date_vente']
    readonly_fields = ['numero_vente', 'montant_total', 'montant_final']
    inlines = [LigneVenteInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('numero_vente', 'statut', 'date_vente')
        }),
        ('Client', {
            'fields': ('client_nom', 'client_email', 'client_telephone')
        }),
        ('Montants', {
            'fields': ('montant_total', 'remise', 'montant_final', 'mode_paiement')
        }),
        ('Commentaire', {
            'fields': ('commentaire',)
        }),
        ('Statut', {
            'fields': ('is_active',)
        })
    )


@admin.register(LigneVente)
class LigneVenteAdmin(admin.ModelAdmin):
    list_display = [
        'vente', 'produit', 'quantite', 'prix_unitaire', 
        'montant_ligne', 'is_active'
    ]
    list_filter = ['is_active', 'vente__date_vente']
    search_fields = ['vente__numero_vente', 'produit__nom', 'produit__code_produit']
    list_editable = ['is_active']
    ordering = ['-vente__date_vente']
    readonly_fields = ['montant_ligne']
