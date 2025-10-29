from django.db import models
from core.models import BaseModel


class Categorie(BaseModel):
    """
    Modèle pour les catégories de produits
    """
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom de la catégorie",
        help_text="Nom de la catégorie de produit"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Description de la catégorie"
    )
    couleur = models.CharField(
        max_length=7,
        default="#3B82F6",
        verbose_name="Couleur",
        help_text="Couleur hexadécimale pour l'affichage"
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Produit(BaseModel):
    """
    Modèle pour les produits
    """
    CATEGORIES_UNITE = [
        ('PIECE', 'Pièce'),
        ('KG', 'Kilogramme'),
        ('L', 'Litre'),
        ('M', 'Mètre'),
        ('M2', 'Mètre carré'),
        ('M3', 'Mètre cube'),
        ('BOITE', 'Boîte'),
        ('PAQUET', 'Paquet'),
    ]

    code_produit = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code produit",
        help_text="Code unique du produit"
    )
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom du produit",
        help_text="Nom du produit"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Description détaillée du produit"
    )
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name='produits',
        verbose_name="Catégorie",
        help_text="Catégorie du produit"
    )
    prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix d'achat",
        help_text="Prix d'achat unitaire"
    )
    prix_vente = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix de vente",
        help_text="Prix de vente unitaire"
    )
    unite = models.CharField(
        max_length=10,
        choices=CATEGORIES_UNITE,
        default='PIECE',
        verbose_name="Unité",
        help_text="Unité de mesure du produit"
    )
    seuil_alerte = models.PositiveIntegerField(
        default=10,
        verbose_name="Seuil d'alerte",
        help_text="Seuil minimum pour déclencher une alerte"
    )
    image = models.ImageField(
        upload_to='produits/',
        blank=True,
        null=True,
        verbose_name="Image",
        help_text="Image du produit"
    )
    fournisseur_principal = models.ForeignKey(
        'fournisseurs.Fournisseur',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produits_principaux',
        verbose_name="Fournisseur principal",
        help_text="Fournisseur principal du produit"
    )

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['nom']

    def __str__(self):
        return f"{self.code_produit} - {self.nom}"

    @property
    def stock_actuel(self):
        """
        Retourne le stock actuel du produit
        """
        from stocks.models import MouvementStock
        mouvements = MouvementStock.objects.filter(produit=self, is_active=True)
        stock_entree = mouvements.filter(type_mouvement='ENTREE').aggregate(
            total=models.Sum('quantite')
        )['total'] or 0
        stock_sortie = mouvements.filter(type_mouvement='SORTIE').aggregate(
            total=models.Sum('quantite')
        )['total'] or 0
        return stock_entree - stock_sortie

    @property
    def est_en_rupture(self):
        """
        Vérifie si le produit est en rupture de stock
        """
        return self.stock_actuel <= self.seuil_alerte

    @property
    def marge_beneficiaire(self):
        """
        Calcule la marge bénéficiaire
        """
        if self.prix_achat > 0:
            return ((self.prix_vente - self.prix_achat) / self.prix_achat) * 100
        return 0