from produits.models import Produit
from .models import CompanySettings


def company_settings_context(request):
    """
    Context processor pour ajouter les informations de l'entreprise à tous les templates
    """
    try:
        company_settings = CompanySettings.get_settings()
        return {
            'company_settings': company_settings
        }
    except Exception:
        return {
            'company_settings': None
        }


def alertes_context(request):
    """
    Context processor pour ajouter les alertes de stock à tous les templates
    """
    if request.user.is_authenticated:
        # Alertes de stock
        alertes_stock = []
        for produit in Produit.objects.filter(is_active=True):
            stock_actuel = produit.stock_actuel
            if stock_actuel <= produit.seuil_alerte:
                alertes_stock.append({
                    'produit': produit,
                    'stock_actuel': stock_actuel,
                    'seuil': produit.seuil_alerte
                })
        
        return {
            'alertes_stock': alertes_stock,
            'alertes_count': len(alertes_stock)
        }
    return {
        'alertes_stock': [],
        'alertes_count': 0
    }


