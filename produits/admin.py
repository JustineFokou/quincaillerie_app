from django.contrib import admin
from .models import Categorie, Produit


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description', 'couleur', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['nom', 'description']
    list_editable = ['is_active']
    ordering = ['nom']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = [
        'code_produit', 'nom', 'categorie', 'prix_achat', 
        'prix_vente', 'stock_actuel', 'seuil_alerte', 'est_en_rupture', 'is_active'
    ]
    list_filter = ['categorie', 'unite', 'is_active', 'created_at']
    search_fields = ['code_produit', 'nom', 'description']
    list_editable = ['prix_achat', 'prix_vente', 'seuil_alerte', 'is_active']
    ordering = ['nom']
    readonly_fields = ['stock_actuel', 'est_en_rupture', 'marge_beneficiaire']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('code_produit', 'nom', 'description', 'categorie', 'unite')
        }),
        ('Prix et stock', {
            'fields': ('prix_achat', 'prix_vente', 'seuil_alerte', 'stock_actuel', 'est_en_rupture', 'marge_beneficiaire')
        }),
        ('Fournisseur et image', {
            'fields': ('fournisseur_principal', 'image')
        }),
        ('Statut', {
            'fields': ('is_active',)
        })
    )
