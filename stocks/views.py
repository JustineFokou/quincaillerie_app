from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse

from .models import MouvementStock
from produits.models import Produit
from fournisseurs.models import Fournisseur


class MouvementStockListView(LoginRequiredMixin, ListView):
    model = MouvementStock
    template_name = 'stocks/list.html'
    context_object_name = 'mouvements'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = MouvementStock.objects.filter(is_active=True).select_related('produit', 'fournisseur')
        
        # Filtrage par recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(produit__nom__icontains=search) |
                Q(produit__code_produit__icontains=search) |
                Q(reference__icontains=search) |
                Q(commentaire__icontains=search)
            )
        
        # Filtrage par type de mouvement
        type_mouvement = self.request.GET.get('type_mouvement')
        if type_mouvement:
            queryset = queryset.filter(type_mouvement=type_mouvement)
        
        # Filtrage par motif
        motif = self.request.GET.get('motif')
        if motif:
            queryset = queryset.filter(motif=motif)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['type_filter'] = self.request.GET.get('type_mouvement', '')
        context['motif_filter'] = self.request.GET.get('motif', '')
        context['type_choices'] = MouvementStock.TYPE_MOUVEMENT_CHOICES
        context['motif_choices'] = MouvementStock.MOTIF_CHOICES
        return context


class MouvementStockDetailView(LoginRequiredMixin, DetailView):
    model = MouvementStock
    template_name = 'stocks/detail.html'
    context_object_name = 'mouvement'
    
    def get_queryset(self):
        return MouvementStock.objects.filter(is_active=True).select_related('produit', 'fournisseur')


class MouvementStockCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'stocks/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produits'] = Produit.objects.filter(is_active=True)
        context['fournisseurs'] = Fournisseur.objects.filter(is_active=True)
        context['type_choices'] = MouvementStock.TYPE_MOUVEMENT_CHOICES
        context['motif_choices'] = MouvementStock.MOTIF_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            produit_id = request.POST.get('produit')
            quantite = int(request.POST.get('quantite', 0))
            motif = request.POST.get('motif')
            reference = request.POST.get('reference', '')
            prix_unitaire = float(request.POST.get('prix_unitaire', 0))
            fournisseur_id = request.POST.get('fournisseur')
            client = request.POST.get('client', '')
            commentaire = request.POST.get('commentaire', '')
            
            produit = get_object_or_404(Produit, id=produit_id, is_active=True)
            fournisseur = None
            if fournisseur_id:
                fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id, is_active=True)
            
            MouvementStock.objects.create(
                produit=produit,
                quantite=quantite,
                motif=motif,
                reference=reference,
                prix_unitaire=prix_unitaire,
                fournisseur=fournisseur,
                client=client,
                commentaire=commentaire,
                date_mouvement=timezone.now()
            )
            
            messages.success(request, 'Mouvement de stock créé avec succès.')
            return redirect('stocks:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            return self.get(request, *args, **kwargs)


class EntreeStockView(LoginRequiredMixin, TemplateView):
    template_name = 'stocks/entree_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produits'] = Produit.objects.filter(is_active=True)
        context['fournisseurs'] = Fournisseur.objects.filter(is_active=True)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            produit_id = request.POST.get('produit')
            quantite = int(request.POST.get('quantite', 0))
            reference = request.POST.get('reference', '')
            prix_unitaire = float(request.POST.get('prix_unitaire', 0))
            fournisseur_id = request.POST.get('fournisseur')
            commentaire = request.POST.get('commentaire', '')
            
            produit = get_object_or_404(Produit, id=produit_id, is_active=True)
            fournisseur = None
            if fournisseur_id:
                fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id, is_active=True)
            
            MouvementStock.objects.create(
                produit=produit,
                type_mouvement='ENTREE',
                quantite=quantite,
                motif='ACHAT',
                reference=reference,
                prix_unitaire=prix_unitaire,
                fournisseur=fournisseur,
                commentaire=commentaire,
                date_mouvement=timezone.now()
            )
            
            messages.success(request, 'Entrée de stock enregistrée avec succès.')
            return redirect('stocks:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'enregistrement : {str(e)}')
            return self.get(request, *args, **kwargs)


class SortieStockView(LoginRequiredMixin, TemplateView):
    template_name = 'stocks/sortie_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produits'] = Produit.objects.filter(is_active=True)
        context['motif_choices'] = [
            choice for choice in MouvementStock.MOTIF_CHOICES 
            if choice[0] in ['VENTE', 'RETOUR_CLIENT', 'CASSAGE', 'PERDU', 'VOL', 'DON']
        ]
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            produit_id = request.POST.get('produit')
            quantite = int(request.POST.get('quantite', 0))
            motif = request.POST.get('motif')
            reference = request.POST.get('reference', '')
            prix_unitaire = float(request.POST.get('prix_unitaire', 0))
            client = request.POST.get('client', '')
            commentaire = request.POST.get('commentaire', '')
            
            produit = get_object_or_404(Produit, id=produit_id, is_active=True)
            
            MouvementStock.objects.create(
                produit=produit,
                type_mouvement='SORTIE',
                quantite=quantite,
                motif=motif,
                reference=reference,
                prix_unitaire=prix_unitaire,
                client=client,
                commentaire=commentaire,
                date_mouvement=timezone.now()
            )
            
            messages.success(request, 'Sortie de stock enregistrée avec succès.')
            return redirect('stocks:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'enregistrement : {str(e)}')
            return self.get(request, *args, **kwargs)


class AjustementStockView(LoginRequiredMixin, TemplateView):
    template_name = 'stocks/ajustement_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produits'] = Produit.objects.filter(is_active=True)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            produit_id = request.POST.get('produit')
            quantite = int(request.POST.get('quantite', 0))
            reference = request.POST.get('reference', '')
            commentaire = request.POST.get('commentaire', '')
            
            produit = get_object_or_404(Produit, id=produit_id, is_active=True)
            
            MouvementStock.objects.create(
                produit=produit,
                type_mouvement='AJUSTEMENT',
                quantite=quantite,
                motif='AJUSTEMENT_INVENTAIRE',
                reference=reference,
                commentaire=commentaire,
                date_mouvement=timezone.now()
            )
            
            messages.success(request, 'Ajustement de stock enregistré avec succès.')
            return redirect('stocks:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'enregistrement : {str(e)}')
            return self.get(request, *args, **kwargs)
