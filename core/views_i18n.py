from django.shortcuts import redirect
from django.views import View
from django.utils import translation
from django.http import HttpResponseRedirect
from django.conf import settings

class SetLanguageView(View):
    """
    Vue pour changer la langue de l'application
    Accepte à la fois GET et POST
    """
    def get(self, request, *args, **kwargs):
        """Gère les requêtes GET (via URL ou lien)"""
        language = request.GET.get('language', 'fr')
        return self._set_language(request, language)
    
    def post(self, request, *args, **kwargs):
        """Gère les requêtes POST (via formulaire)"""
        language = request.POST.get('language', 'fr')
        return self._set_language(request, language)
    
    def _set_language(self, request, language):
        """Méthode helper pour définir la langue"""
        if language in dict(settings.LANGUAGES).keys():
            translation.activate(language)
            # Utiliser 'django_language' comme clé de session (compatible Django 5.2)
            request.session['django_language'] = language
            next_url = request.GET.get('next') or request.POST.get('next') or request.META.get('HTTP_REFERER', '/')
            response = HttpResponseRedirect(next_url)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language, max_age=365*24*60*60)  # Cookie valide 1 an
            return response
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

