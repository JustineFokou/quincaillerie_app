from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Produit, Categorie
from fournisseurs.models import Fournisseur


class ProduitListView(LoginRequiredMixin, ListView):
    model = Produit
    template_name = 'produits/list.html'
    context_object_name = 'produits'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Produit.objects.filter(is_active=True).select_related('categorie', 'fournisseur_principal')
        
        # Filtrage par recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search) |
                Q(code_produit__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Filtrage par catégorie
        categorie_id = self.request.GET.get('categorie')
        if categorie_id:
            queryset = queryset.filter(categorie_id=categorie_id)
        
        # Filtrage par rupture de stock
        rupture = self.request.GET.get('rupture')
        if rupture == 'true':
            queryset = [p for p in queryset if p.est_en_rupture]
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.filter(is_active=True)
        context['search'] = self.request.GET.get('search', '')
        context['categorie_filter'] = self.request.GET.get('categorie', '')
        context['rupture_filter'] = self.request.GET.get('rupture', '')
        return context


class ProduitDetailView(LoginRequiredMixin, DetailView):
    model = Produit
    template_name = 'produits/detail.html'
    context_object_name = 'produit'
    
    def get_queryset(self):
        return Produit.objects.filter(is_active=True).select_related('categorie', 'fournisseur_principal')


class ProduitCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'produits/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.filter(is_active=True)
        context['fournisseurs'] = Fournisseur.objects.filter(is_active=True)
        context['unite_choices'] = Produit.CATEGORIES_UNITE
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            code_produit = request.POST.get('code_produit')
            nom = request.POST.get('nom')
            description = request.POST.get('description', '')
            categorie_id = request.POST.get('categorie')
            prix_achat = float(request.POST.get('prix_achat', 0))
            prix_vente = float(request.POST.get('prix_vente', 0))
            unite = request.POST.get('unite')
            seuil_alerte = int(request.POST.get('seuil_alerte', 10))
            fournisseur_id = request.POST.get('fournisseur')
            
            categorie = get_object_or_404(Categorie, id=categorie_id, is_active=True)
            fournisseur = None
            if fournisseur_id:
                fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id, is_active=True)
            
            Produit.objects.create(
                code_produit=code_produit,
                nom=nom,
                description=description,
                categorie=categorie,
                prix_achat=prix_achat,
                prix_vente=prix_vente,
                unite=unite,
                seuil_alerte=seuil_alerte,
                fournisseur_principal=fournisseur
            )
            
            messages.success(request, 'Produit créé avec succès.')
            return redirect('produits:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            return self.get(request, *args, **kwargs)


class ProduitUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'produits/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produit'] = get_object_or_404(Produit, id=self.kwargs['pk'], is_active=True)
        context['categories'] = Categorie.objects.filter(is_active=True)
        context['fournisseurs'] = Fournisseur.objects.filter(is_active=True)
        context['unite_choices'] = Produit.CATEGORIES_UNITE
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            produit = get_object_or_404(Produit, id=self.kwargs['pk'], is_active=True)
            
            produit.code_produit = request.POST.get('code_produit')
            produit.nom = request.POST.get('nom')
            produit.description = request.POST.get('description', '')
            categorie_id = request.POST.get('categorie')
            produit.prix_achat = float(request.POST.get('prix_achat', 0))
            produit.prix_vente = float(request.POST.get('prix_vente', 0))
            produit.unite = request.POST.get('unite')
            produit.seuil_alerte = int(request.POST.get('seuil_alerte', 10))
            fournisseur_id = request.POST.get('fournisseur')
            
            produit.categorie = get_object_or_404(Categorie, id=categorie_id, is_active=True)
            produit.fournisseur_principal = None
            if fournisseur_id:
                produit.fournisseur_principal = get_object_or_404(Fournisseur, id=fournisseur_id, is_active=True)
            
            produit.save()
            
            messages.success(request, 'Produit modifié avec succès.')
            return redirect('produits:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            return self.get(request, *args, **kwargs)


class ProduitDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'produits/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produit'] = get_object_or_404(Produit, id=self.kwargs['pk'], is_active=True)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            produit = get_object_or_404(Produit, id=self.kwargs['pk'], is_active=True)
            produit.soft_delete()
            messages.success(request, 'Produit supprimé avec succès.')
            return redirect('produits:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression : {str(e)}')
            return redirect('produits:list')


class CategorieListView(LoginRequiredMixin, ListView):
    model = Categorie
    template_name = 'produits/categorie_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Categorie.objects.filter(is_active=True)


class CategorieCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'produits/categorie_form.html'
    
    def post(self, request, *args, **kwargs):
        try:
            nom = request.POST.get('nom')
            description = request.POST.get('description', '')
            couleur = request.POST.get('couleur', '#3B82F6')
            
            Categorie.objects.create(
                nom=nom,
                description=description,
                couleur=couleur
            )
            
            messages.success(request, 'Catégorie créée avec succès.')
            return redirect('produits:categorie_list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            return self.get(request, *args, **kwargs)
