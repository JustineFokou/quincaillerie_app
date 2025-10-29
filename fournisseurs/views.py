from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Fournisseur


class FournisseurListView(LoginRequiredMixin, ListView):
    model = Fournisseur
    template_name = 'fournisseurs/list.html'
    context_object_name = 'fournisseurs'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Fournisseur.objects.filter(is_active=True)
        
        # Filtrage par recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search) |
                Q(contact__icontains=search) |
                Q(email__icontains=search) |
                Q(ville__icontains=search)
            )
        
        # Filtrage par pays
        pays = self.request.GET.get('pays')
        if pays:
            queryset = queryset.filter(pays=pays)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['pays_filter'] = self.request.GET.get('pays', '')
        context['pays_choices'] = Fournisseur.objects.filter(is_active=True).values_list('pays', flat=True).distinct()
        return context


class FournisseurDetailView(LoginRequiredMixin, DetailView):
    model = Fournisseur
    template_name = 'fournisseurs/detail.html'
    context_object_name = 'fournisseur'
    
    def get_queryset(self):
        return Fournisseur.objects.filter(is_active=True)


class FournisseurCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'fournisseurs/form.html'
    
    def post(self, request, *args, **kwargs):
        try:
            nom = request.POST.get('nom')
            contact = request.POST.get('contact')
            email = request.POST.get('email')
            telephone = request.POST.get('telephone')
            adresse = request.POST.get('adresse')
            ville = request.POST.get('ville')
            code_postal = request.POST.get('code_postal')
            pays = request.POST.get('pays', 'France')
            numero_tva = request.POST.get('numero_tva', '')
            conditions_paiement = request.POST.get('conditions_paiement', '30 jours')
            delai_livraison = int(request.POST.get('delai_livraison', 7))
            note = request.POST.get('note', '')
            
            Fournisseur.objects.create(
                nom=nom,
                contact=contact,
                email=email,
                telephone=telephone,
                adresse=adresse,
                ville=ville,
                code_postal=code_postal,
                pays=pays,
                numero_tva=numero_tva,
                conditions_paiement=conditions_paiement,
                delai_livraison=delai_livraison,
                note=note
            )
            
            messages.success(request, 'Fournisseur créé avec succès.')
            return redirect('fournisseurs:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            return self.get(request, *args, **kwargs)


class FournisseurUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'fournisseurs/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fournisseur'] = get_object_or_404(Fournisseur, id=self.kwargs['pk'], is_active=True)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            fournisseur = get_object_or_404(Fournisseur, id=self.kwargs['pk'], is_active=True)
            
            fournisseur.nom = request.POST.get('nom')
            fournisseur.contact = request.POST.get('contact')
            fournisseur.email = request.POST.get('email')
            fournisseur.telephone = request.POST.get('telephone')
            fournisseur.adresse = request.POST.get('adresse')
            fournisseur.ville = request.POST.get('ville')
            fournisseur.code_postal = request.POST.get('code_postal')
            fournisseur.pays = request.POST.get('pays', 'France')
            fournisseur.numero_tva = request.POST.get('numero_tva', '')
            fournisseur.conditions_paiement = request.POST.get('conditions_paiement', '30 jours')
            fournisseur.delai_livraison = int(request.POST.get('delai_livraison', 7))
            fournisseur.note = request.POST.get('note', '')
            
            fournisseur.save()
            
            messages.success(request, 'Fournisseur modifié avec succès.')
            return redirect('fournisseurs:detail', pk=fournisseur.pk)
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            return self.get(request, *args, **kwargs)


class FournisseurDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'fournisseurs/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fournisseur'] = get_object_or_404(Fournisseur, id=self.kwargs['pk'], is_active=True)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            fournisseur = get_object_or_404(Fournisseur, id=self.kwargs['pk'], is_active=True)
            fournisseur.soft_delete()
            messages.success(request, 'Fournisseur supprimé avec succès.')
            return redirect('fournisseurs:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression : {str(e)}')
            return redirect('fournisseurs:list')
