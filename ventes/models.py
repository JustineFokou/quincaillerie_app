from django.db import models
from core.models import BaseModel


class Vente(BaseModel):
    """
    Modèle pour les ventes
    """
    STATUT_CHOICES = [
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ]

    numero_vente = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro de vente",
        help_text="Numéro unique de la vente"
    )
    client_nom = models.CharField(
        max_length=200,
        verbose_name="Nom du client",
        help_text="Nom du client"
    )
    client_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email du client",
        help_text="Email du client"
    )
    client_telephone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Téléphone du client",
        help_text="Téléphone du client"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_COURS',
        verbose_name="Statut",
        help_text="Statut de la vente"
    )
    date_vente = models.DateTimeField(
        verbose_name="Date de vente",
        help_text="Date et heure de la vente"
    )
    montant_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Montant total",
        help_text="Montant total de la vente"
    )
    remise = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Remise",
        help_text="Montant de la remise"
    )
    montant_final = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Montant final",
        help_text="Montant final après remise"
    )
    mode_paiement = models.CharField(
        max_length=50,
        default='ESPECES',
        verbose_name="Mode de paiement",
        help_text="Mode de paiement"
    )
    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire",
        help_text="Commentaire sur la vente"
    )

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ['-date_vente']

    def __str__(self):
        return f"Vente {self.numero_vente} - {self.client_nom}"

    def save(self, *args, **kwargs):
        if not self.date_vente:
            from django.utils import timezone
            self.date_vente = timezone.now()
        
        # Générer le numéro de vente s'il n'existe pas
        if not self.numero_vente:
            from django.utils import timezone
            now = timezone.now()
            self.numero_vente = f"V{now.strftime('%Y%m%d%H%M%S')}"
        
        # Calculer le montant final
        self.montant_final = self.montant_total - self.remise
        
        super().save(*args, **kwargs)


class LigneVente(BaseModel):
    """
    Modèle pour les lignes de vente
    """
    vente = models.ForeignKey(
        Vente,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name="Vente",
        help_text="Vente associée"
    )
    produit = models.ForeignKey(
        'produits.Produit',
        on_delete=models.CASCADE,
        verbose_name="Produit",
        help_text="Produit vendu"
    )
    quantite = models.PositiveIntegerField(
        verbose_name="Quantité",
        help_text="Quantité vendue"
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix unitaire",
        help_text="Prix unitaire au moment de la vente"
    )
    montant_ligne = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Montant de la ligne",
        help_text="Montant total de la ligne"
    )

    class Meta:
        verbose_name = "Ligne de vente"
        verbose_name_plural = "Lignes de vente"
        ordering = ['id']

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"

    def save(self, *args, **kwargs):
        # Calculer le montant de la ligne
        self.montant_ligne = self.prix_unitaire * self.quantite
        
        super().save(*args, **kwargs)
        
        # Mettre à jour le montant total de la vente
        self.vente.montant_total = sum(
            ligne.montant_ligne for ligne in self.vente.lignes.all()
        )
        self.vente.save(update_fields=['montant_total', 'montant_final'])
