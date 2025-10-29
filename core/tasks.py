from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from produits.models import Produit
from stocks.models import MouvementStock
from django.utils import timezone


@shared_task
def check_stock_alerts():
    """
    Vérifie les produits en rupture de stock et envoie des alertes
    """
    produits_en_rupture = []
    
    for produit in Produit.objects.filter(is_active=True):
        if produit.est_en_rupture:
            produits_en_rupture.append({
                'nom': produit.nom,
                'code': produit.code_produit,
                'stock_actuel': produit.stock_actuel,
                'seuil': produit.seuil_alerte,
                'fournisseur': produit.fournisseur_principal.nom if produit.fournisseur_principal else 'Non défini'
            })
    
    if produits_en_rupture:
        # Envoyer un email d'alerte (en développement, affiché dans la console)
        message = "Alertes de stock - Produits en rupture :\n\n"
        for produit in produits_en_rupture:
            message += f"- {produit['nom']} ({produit['code']}) : {produit['stock_actuel']} unités (seuil: {produit['seuil']})\n"
            message += f"  Fournisseur: {produit['fournisseur']}\n\n"
        
        print("=" * 50)
        print("ALERTE DE STOCK")
        print("=" * 50)
        print(message)
        print("=" * 50)
        
        # En production, envoyer un email
        if not settings.DEBUG:
            send_mail(
                subject='Alertes de Stock - Quincaillerie',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['admin@quincaillerie.com'],
                fail_silently=False,
            )
    
    return f"{len(produits_en_rupture)} produits en rupture de stock détectés"


@shared_task
def generate_daily_report():
    """
    Génère un rapport quotidien des ventes et mouvements de stock
    """
    today = timezone.now().date()
    
    # Statistiques des ventes du jour
    ventes_jour = MouvementStock.objects.filter(
        type_mouvement='SORTIE',
        motif='VENTE',
        date_mouvement__date=today,
        is_active=True
    )
    
    ca_jour = sum(mouvement.valeur_totale for mouvement in ventes_jour if mouvement.valeur_totale)
    nb_ventes = len(set(mouvement.reference for mouvement in ventes_jour if mouvement.reference))
    
    # Mouvements de stock du jour
    mouvements_entree = MouvementStock.objects.filter(
        type_mouvement='ENTREE',
        date_mouvement__date=today,
        is_active=True
    ).count()
    
    mouvements_sortie = MouvementStock.objects.filter(
        type_mouvement='SORTIE',
        date_mouvement__date=today,
        is_active=True
    ).count()
    
    report = f"""
RAPPORT QUOTIDIEN - {today.strftime('%d/%m/%Y')}
===============================================

VENTES :
- Chiffre d'affaires : {ca_jour:.2f} €
- Nombre de ventes : {nb_ventes}

STOCK :
- Entrées : {mouvements_entree}
- Sorties : {mouvements_sortie}

===============================================
    """
    
    print(report)
    
    return {
        'date': today,
        'ca_jour': ca_jour,
        'nb_ventes': nb_ventes,
        'mouvements_entree': mouvements_entree,
        'mouvements_sortie': mouvements_sortie
    }
