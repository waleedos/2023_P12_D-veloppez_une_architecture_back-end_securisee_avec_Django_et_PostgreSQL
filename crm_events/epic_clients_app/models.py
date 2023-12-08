from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from epic_auth_app.models import Utilisateur


class Client(models.Model):
    # Définition du modèle Client pour représenter les clients dans la base de données

    class Role(models.TextChoices):
        # Classe interne pour définir les choix de rôle pour le client
        PROSPECT = 'PR', _('Prospect')  # Client potentiel
        CLIENT = 'CL', _('Client')  # Client confirmé

    # Définition des champs du modèle Client
    full_name = models.CharField(_('nom complet'), max_length=255)  # Nom complet du client
    email = models.EmailField(_('email'), unique=True)  # Adresse email du client, unique pour chaque client
    phone_number = models.CharField(_('téléphone'), max_length=20)  # Numéro de téléphone du client
    company_name = models.CharField(_('nom de l’entreprise'), max_length=255)  # Nom de l'entreprise du client

    # Date de création de l'enregistrement client
    created_at = models.DateTimeField(_('date de création'), default=timezone.now)

    # Date de la dernière mise à jour de l'enregistrement
    updated_at = models.DateTimeField(_('dernière mise à jour'), auto_now=True)

    # Clé étrangère liant le client à un utilisateur (commercial chez Epic Events)
    sales_contact = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients_commercial',
        verbose_name=_('contact commercial chez Epic Events')
    )
    # Rôle du client, avec une valeur par défaut de 'Prospect'
    role = models.CharField(_('rôle'), max_length=2, choices=Role.choices, default=Role.PROSPECT)

    # Nouveau champ pour le commercial assigné
    commercial_assigne = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients_assignes',
        verbose_name=_('Commercial Assigné')
    )
    # Ce champ relie le client à un utilisateur (commercial), qui est assigné à ce client

    def __str__(self):
        # Méthode pour la représentation en chaîne de caractères du client
        return self.full_name  # Retourne le nom complet du client
