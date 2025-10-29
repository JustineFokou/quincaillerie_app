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
