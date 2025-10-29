from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from produits.models import Produit, Categorie
from stocks.models import MouvementStock
from ventes.models import Vente
from fournisseurs.models import Fournisseur


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques générales
        context['total_produits'] = Produit.objects.filter(is_active=True).count()
        context['total_categories'] = Categorie.objects.filter(is_active=True).count()
        context['total_fournisseurs'] = Fournisseur.objects.filter(is_active=True).count()
        context['total_ventes'] = Vente.objects.filter(is_active=True).count()
        
        # Produits en rupture de stock
        context['produits_rupture'] = Produit.objects.filter(
            is_active=True
        ).extra(
            where=["id IN (SELECT produit_id FROM stocks_mouvementstock WHERE is_active=True GROUP BY produit_id HAVING SUM(CASE WHEN type_mouvement='ENTREE' THEN quantite ELSE -quantite END) <= seuil_alerte)"]
        )[:10]
        
        # Ventes récentes
        context['ventes_recentes'] = Vente.objects.filter(
            is_active=True
        ).order_by('-date_vente')[:5]
        
        # Mouvements de stock récents
        context['mouvements_recents'] = MouvementStock.objects.filter(
            is_active=True
        ).order_by('-date_mouvement')[:10]
        
        # Statistiques des ventes du mois
        debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ventes_mois = Vente.objects.filter(
            is_active=True,
            date_vente__gte=debut_mois
        )
        
        context['ca_mois'] = ventes_mois.aggregate(
            total=Sum('montant_final')
        )['total'] or 0
        
        context['nb_ventes_mois'] = ventes_mois.count()
        
        # Top 5 des produits les plus vendus
        context['top_produits'] = Produit.objects.filter(
            is_active=True,
            ventes__lignes__vente__is_active=True
        ).annotate(
            total_vendu=Sum('ventes__lignes__quantite')
        ).order_by('-total_vendu')[:5]
        
        # Alertes de stock
        context['alertes_stock'] = []
        for produit in Produit.objects.filter(is_active=True):
            stock_actuel = produit.stock_actuel
            if stock_actuel <= produit.seuil_alerte:
                context['alertes_stock'].append({
                    'produit': produit,
                    'stock_actuel': stock_actuel,
                    'seuil': produit.seuil_alerte
                })
        
        return context
