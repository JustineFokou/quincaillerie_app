from django.db import models
from core.models import BaseModel


class MouvementStock(BaseModel):
    """
    Modèle pour les mouvements de stock
    """
    TYPE_MOUVEMENT_CHOICES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
        ('AJUSTEMENT', 'Ajustement'),
        ('RETOUR', 'Retour'),
    ]

    MOTIF_CHOICES = [
        ('ACHAT', 'Achat'),
        ('VENTE', 'Vente'),
        ('AJUSTEMENT_INVENTAIRE', 'Ajustement inventaire'),
        ('RETOUR_CLIENT', 'Retour client'),
        ('RETOUR_FOURNISSEUR', 'Retour fournisseur'),
        ('CASSAGE', 'Cassage'),
        ('PERDU', 'Perdu'),
        ('VOL', 'Vol'),
        ('DON', 'Don'),
    ]

    produit = models.ForeignKey(
        'produits.Produit',
        on_delete=models.CASCADE,
        related_name='mouvements_stock',
        verbose_name="Produit",
        help_text="Produit concerné par le mouvement"
    )
    type_mouvement = models.CharField(
        max_length=20,
        choices=TYPE_MOUVEMENT_CHOICES,
        verbose_name="Type de mouvement",
        help_text="Type de mouvement de stock"
    )
    quantite = models.PositiveIntegerField(
        verbose_name="Quantité",
        help_text="Quantité concernée par le mouvement"
    )
    motif = models.CharField(
        max_length=30,
        choices=MOTIF_CHOICES,
        verbose_name="Motif",
        help_text="Motif du mouvement"
    )
    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Référence",
        help_text="Référence du document (facture, bon de commande, etc.)"
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Prix unitaire",
        help_text="Prix unitaire au moment du mouvement"
    )
    fournisseur = models.ForeignKey(
        'fournisseurs.Fournisseur',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mouvements_stock',
        verbose_name="Fournisseur",
        help_text="Fournisseur concerné (pour les entrées)"
    )
    client = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Client",
        help_text="Client concerné (pour les sorties)"
    )
    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire",
        help_text="Commentaire sur le mouvement"
    )
    date_mouvement = models.DateTimeField(
        verbose_name="Date du mouvement",
        help_text="Date et heure du mouvement"
    )

    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-date_mouvement']

    def __str__(self):
        return f"{self.produit.nom} - {self.get_type_mouvement_display()} - {self.quantite}"

    def save(self, *args, **kwargs):
        if not self.date_mouvement:
            from django.utils import timezone
            self.date_mouvement = timezone.now()
        super().save(*args, **kwargs)

    @property
    def valeur_totale(self):
        """
        Calcule la valeur totale du mouvement
        """
        if self.prix_unitaire:
            return self.prix_unitaire * self.quantite
        return 0