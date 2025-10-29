from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

from .models import Vente, LigneVente
from produits.models import Produit


class VenteListView(LoginRequiredMixin, ListView):
    model = Vente
    template_name = 'ventes/list.html'
    context_object_name = 'ventes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Vente.objects.filter(is_active=True)
        
        # Filtrage par recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(numero_vente__icontains=search) |
                Q(client_nom__icontains=search) |
                Q(client_email__icontains=search)
            )
        
        # Filtrage par statut
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['statut_filter'] = self.request.GET.get('statut', '')
        context['statut_choices'] = Vente.STATUT_CHOICES
        return context


class VenteDetailView(LoginRequiredMixin, DetailView):
    model = Vente
    template_name = 'ventes/detail.html'
    context_object_name = 'vente'
    
    def get_queryset(self):
        return Vente.objects.filter(is_active=True)


class VenteCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'ventes/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produits'] = Produit.objects.filter(is_active=True)
        context['statut_choices'] = Vente.STATUT_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            client_nom = request.POST.get('client_nom')
            client_email = request.POST.get('client_email', '')
            client_telephone = request.POST.get('client_telephone', '')
            mode_paiement = request.POST.get('mode_paiement', 'ESPECES')
            commentaire = request.POST.get('commentaire', '')
            
            vente = Vente.objects.create(
                client_nom=client_nom,
                client_email=client_email,
                client_telephone=client_telephone,
                mode_paiement=mode_paiement,
                commentaire=commentaire,
                date_vente=timezone.now()
            )
            
            messages.success(request, 'Vente créée avec succès.')
            return redirect('ventes:detail', pk=vente.pk)
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            return self.get(request, *args, **kwargs)


class VenteUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'ventes/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vente'] = get_object_or_404(Vente, id=self.kwargs['pk'], is_active=True)
        context['statut_choices'] = Vente.STATUT_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            vente = get_object_or_404(Vente, id=self.kwargs['pk'], is_active=True)
            
            vente.client_nom = request.POST.get('client_nom')
            vente.client_email = request.POST.get('client_email', '')
            vente.client_telephone = request.POST.get('client_telephone', '')
            vente.statut = request.POST.get('statut', 'EN_COURS')
            vente.mode_paiement = request.POST.get('mode_paiement', 'ESPECES')
            vente.remise = float(request.POST.get('remise', 0))
            vente.commentaire = request.POST.get('commentaire', '')
            
            vente.save()
            
            messages.success(request, 'Vente modifiée avec succès.')
            return redirect('ventes:detail', pk=vente.pk)
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            return self.get(request, *args, **kwargs)


class VenteDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'ventes/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vente'] = get_object_or_404(Vente, id=self.kwargs['pk'], is_active=True)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            vente = get_object_or_404(Vente, id=self.kwargs['pk'], is_active=True)
            vente.soft_delete()
            messages.success(request, 'Vente supprimée avec succès.')
            return redirect('ventes:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression : {str(e)}')
            return redirect('ventes:list')


class VenteFinaliserView(LoginRequiredMixin, TemplateView):
    template_name = 'ventes/finaliser.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vente'] = get_object_or_404(Vente, id=self.kwargs['pk'], is_active=True)
        context['produits'] = Produit.objects.filter(is_active=True)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            vente = get_object_or_404(Vente, id=self.kwargs['pk'], is_active=True)
            
            # Ajouter des lignes de vente
            produits_ids = request.POST.getlist('produits')
            quantites = request.POST.getlist('quantites')
            
            for produit_id, quantite in zip(produits_ids, quantites):
                if quantite and int(quantite) > 0:
                    produit = get_object_or_404(Produit, id=produit_id, is_active=True)
                    LigneVente.objects.create(
                        vente=vente,
                        produit=produit,
                        quantite=int(quantite),
                        prix_unitaire=produit.prix_vente
                    )
            
            vente.statut = 'TERMINEE'
            vente.save()
            
            messages.success(request, 'Vente finalisée avec succès.')
            return redirect('ventes:detail', pk=vente.pk)
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la finalisation : {str(e)}')
            return self.get(request, *args, **kwargs)
