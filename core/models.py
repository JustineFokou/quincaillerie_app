from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Modèle de base avec des champs communs pour tous les modèles
    """
    created_at = models.DateTimeField(
        verbose_name="Date de création",
        auto_now_add=True,
        help_text="Date et heure de création de l'enregistrement"
    )
    updated_at = models.DateTimeField(
        verbose_name="Date de modification",
        auto_now=True,
        help_text="Date et heure de dernière modification"
    )
    is_active = models.BooleanField(
        verbose_name="Actif",
        default=True,
        help_text="Indique si l'enregistrement est actif"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self):
        """
        Suppression logique de l'enregistrement
        """
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])

    def restore(self):
        """
        Restauration d'un enregistrement supprimé logiquement
        """
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])

    def __str__(self):
        return f"{self.__class__.__name__} - {self.pk}"


class TimestampedModel(BaseModel):
    """
    Modèle avec timestamps et gestion des utilisateurs
    """
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name="Créé par",
        help_text="Utilisateur qui a créé l'enregistrement"
    )
    updated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name="Modifié par",
        help_text="Utilisateur qui a modifié l'enregistrement"
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Logique pour capturer l'utilisateur actuel lors de la sauvegarde
        # Cette logique sera implémentée dans les vues
        super().save(*args, **kwargs)


class CompanySettings(models.Model):
    """
    Modèle pour enregistrer les informations de l'entreprise
    Singleton pattern - une seule instance de ce modèle doit exister
    """
    nom_entreprise = models.CharField(
        max_length=200,
        verbose_name="Nom de l'entreprise",
        help_text="Le nom officiel de votre entreprise"
    )
    slogan = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Slogan",
        help_text="Le slogan de votre entreprise"
    )
    adresse = models.TextField(
        verbose_name="Adresse",
        help_text="Adresse complète de l'entreprise"
    )
    ville = models.CharField(
        max_length=100,
        verbose_name="Ville",
        help_text="Ville où se trouve l'entreprise"
    )
    pays = models.CharField(
        max_length=100,
        default="Haïti",
        verbose_name="Pays",
        help_text="Pays où se trouve l'entreprise"
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
        help_text="Numéro de téléphone principal"
    )
    telephone_secondaire = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Téléphone secondaire",
        help_text="Numéro de téléphone secondaire (optionnel)"
    )
    email = models.EmailField(
        verbose_name="Email",
        help_text="Adresse email de contact"
    )
    site_web = models.URLField(
        blank=True,
        null=True,
        verbose_name="Site web",
        help_text="URL du site web (optionnel)"
    )
    numero_fiscal = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Numéro fiscal",
        help_text="Numéro fiscal/NIF de l'entreprise"
    )
    logo = models.ImageField(
        upload_to='company/',
        blank=True,
        null=True,
        verbose_name="Logo",
        help_text="Logo de l'entreprise"
    )
    devise = models.CharField(
        max_length=10,
        default="HTG",
        verbose_name="Devise",
        help_text="Devise utilisée (HTG, USD, etc.)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Configuration de l'entreprise"
        verbose_name_plural = "Configuration de l'entreprise"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.nom_entreprise}"

    @classmethod
    def load(cls):
        """
        Charge les paramètres de l'entreprise.
        Si aucun n'existe, en crée un avec des valeurs par défaut.
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    @classmethod
    def get_settings(cls):
        """
        Retourne les paramètres de l'entreprise ou None
        """
        try:
            return cls.objects.get(pk=1)
        except cls.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        """
        Force l'ID à 1 pour assurer qu'il n'y a qu'une seule instance
        """
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Empêche la suppression de l'instance singleton
        """
        pass
