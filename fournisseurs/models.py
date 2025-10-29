from django.db import models
from core.models import BaseModel


class Fournisseur(BaseModel):
    """
    Modèle pour les fournisseurs
    """
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom du fournisseur",
        help_text="Nom de l'entreprise fournisseur"
    )
    contact = models.CharField(
        max_length=100,
        verbose_name="Contact",
        help_text="Nom du contact principal"
    )
    email = models.EmailField(
        verbose_name="Email",
        help_text="Adresse email du fournisseur"
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
        help_text="Numéro de téléphone"
    )
    adresse = models.TextField(
        verbose_name="Adresse",
        help_text="Adresse complète du fournisseur"
    )
    ville = models.CharField(
        max_length=100,
        verbose_name="Ville",
        help_text="Ville"
    )
    code_postal = models.CharField(
        max_length=10,
        verbose_name="Code postal",
        help_text="Code postal"
    )
    pays = models.CharField(
        max_length=100,
        default="France",
        verbose_name="Pays",
        help_text="Pays"
    )
    numero_tva = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Numéro TVA",
        help_text="Numéro de TVA intracommunautaire"
    )
    conditions_paiement = models.CharField(
        max_length=100,
        default="30 jours",
        verbose_name="Conditions de paiement",
        help_text="Conditions de paiement"
    )
    delai_livraison = models.PositiveIntegerField(
        default=7,
        verbose_name="Délai de livraison (jours)",
        help_text="Délai de livraison en jours"
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Note",
        help_text="Notes supplémentaires"
    )

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    @property
    def adresse_complete(self):
        """
        Retourne l'adresse complète formatée
        """
        return f"{self.adresse}, {self.code_postal} {self.ville}, {self.pays}"