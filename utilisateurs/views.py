from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.db.models import Q

from .models import User, ProfilUtilisateur


class LoginView(LoginView):
    template_name = 'utilisateurs/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('core:dashboard')


class LogoutView(LogoutView):
    next_page = reverse_lazy('utilisateurs:login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'utilisateurs/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        try:
            context['profil'] = self.request.user.profil
        except ProfilUtilisateur.DoesNotExist:
            context['profil'] = None
        return context


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'utilisateurs/profile_edit.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.telephone = request.POST.get('telephone', '')
            user.adresse = request.POST.get('adresse', '')
            user.save()
            
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('utilisateurs:profile')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la mise à jour : {str(e)}')
            return self.get(request, *args, **kwargs)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'utilisateurs/list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        
        # Filtrage par recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(username__icontains=search)
            )
        
        # Filtrage par rôle
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(role=role)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['role_filter'] = self.request.GET.get('role', '')
        context['role_choices'] = User.ROLE_CHOICES
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'utilisateurs/detail.html'
    context_object_name = 'user_detail'
    
    def get_queryset(self):
        return User.objects.filter(is_active=True)


class UserCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'utilisateurs/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_choices'] = User.ROLE_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            role = request.POST.get('role', 'VENDEUR')
            telephone = request.POST.get('telephone', '')
            adresse = request.POST.get('adresse', '')
            password = request.POST.get('password')
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role,
                telephone=telephone,
                adresse=adresse,
                password=password
            )
            
            messages.success(request, 'Utilisateur créé avec succès.')
            return redirect('utilisateurs:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création : {str(e)}')
            return self.get(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'utilisateurs/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = get_object_or_404(User, id=self.kwargs['pk'], is_active=True)
        context['role_choices'] = User.ROLE_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(User, id=self.kwargs['pk'], is_active=True)
            
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.role = request.POST.get('role', 'VENDEUR')
            user.telephone = request.POST.get('telephone', '')
            user.adresse = request.POST.get('adresse', '')
            
            password = request.POST.get('password')
            if password:
                user.set_password(password)
            
            user.save()
            
            messages.success(request, 'Utilisateur modifié avec succès.')
            return redirect('utilisateurs:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification : {str(e)}')
            return self.get(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'utilisateurs/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = get_object_or_404(User, id=self.kwargs['pk'], is_active=True)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(User, id=self.kwargs['pk'], is_active=True)
            user.is_active = False
            user.save()
            messages.success(request, 'Utilisateur supprimé avec succès.')
            return redirect('utilisateurs:list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression : {str(e)}')
            return redirect('utilisateurs:list')
