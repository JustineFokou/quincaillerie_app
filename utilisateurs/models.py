from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel


class User(AbstractUser):
    """
    Modèle utilisateur étendu avec des rôles spécifiques
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('GERANT', 'Gérant'),
        ('VENDEUR', 'Vendeur'),
        ('STOCKISTE', 'Stockiste'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='VENDEUR',
        verbose_name="Rôle",
        help_text="Rôle de l'utilisateur dans le système"
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Téléphone",
        help_text="Numéro de téléphone"
    )
    adresse = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse",
        help_text="Adresse de l'utilisateur"
    )
    date_embauche = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date d'embauche",
        help_text="Date d'embauche"
    )
    salaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Salaire",
        help_text="Salaire mensuel"
    )
    is_active_employee = models.BooleanField(
        default=True,
        verbose_name="Employé actif",
        help_text="Indique si l'employé est actif"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"

    @property
    def nom_complet(self):
        """
        Retourne le nom complet de l'utilisateur
        """
        return f"{self.first_name} {self.last_name}".strip()

    def has_role(self, role):
        """
        Vérifie si l'utilisateur a un rôle spécifique
        """
        return self.role == role

    def can_manage_stock(self):
        """
        Vérifie si l'utilisateur peut gérer le stock
        """
        return self.role in ['ADMIN', 'GERANT', 'STOCKISTE']

    def can_manage_sales(self):
        """
        Vérifie si l'utilisateur peut gérer les ventes
        """
        return self.role in ['ADMIN', 'GERANT', 'VENDEUR']

    def can_manage_users(self):
        """
        Vérifie si l'utilisateur peut gérer les utilisateurs
        """
        return self.role in ['ADMIN', 'GERANT']


class ProfilUtilisateur(BaseModel):
    """
    Profil étendu pour les utilisateurs
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil',
        verbose_name="Utilisateur",
        help_text="Utilisateur associé"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Avatar",
        help_text="Photo de profil"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Biographie",
        help_text="Description personnelle"
    )
    preferences_notifications = models.JSONField(
        default=dict,
        verbose_name="Préférences notifications",
        help_text="Préférences de notification"
    )
    theme_preference = models.CharField(
        max_length=20,
        default='light',
        choices=[
            ('light', 'Clair'),
            ('dark', 'Sombre'),
            ('auto', 'Automatique'),
        ],
        verbose_name="Thème préféré",
        help_text="Thème d'interface préféré"
    )

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def __str__(self):
        return f"Profil de {self.user.nom_complet}"
