from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from epic_contracts_app.models import Contrat
from epic_auth_app.models import Utilisateur

# Importation des modules nécessaires pour définir les modèles Django.


class Evenement(models.Model):
    # Définition du modèle Evenement, héritant de models.Model de Django.

    class Statut(models.TextChoices):
        # Sous-classe Statut définissant les choix de statuts pour les événements.

        PLANIFIE = 'PL', _('Planifié')
        REALISE = 'RE', _('Réalisé')
        ANNULE = 'AN', _('Annulé')
        # Définition des différents statuts possibles pour un événement.

    nom = models.CharField(_('nom'), max_length=255)
    # Champ pour le nom de l'événement, avec une longueur maximale de 255 caractères.

    contrat = models.ForeignKey(
        Contrat,
        on_delete=models.CASCADE,
        related_name='evenements',
        verbose_name=_('contrat associé'),
    )
    # Clé étrangère vers le modèle Contrat. En cas de suppression d'un Contrat, les événements liés seront supprimés.

    date_debut = models.DateTimeField(_('date de début'), default=timezone.now)
    # Champ pour la date de début de l'événement, avec la date et l'heure actuelles par défaut.

    date_fin = models.DateTimeField(_('date de fin'), default=timezone.now)
    # Champ pour la date de fin de l'événement, avec la date et l'heure actuelles par défaut.

    lieu = models.CharField(_('lieu'), max_length=255)
    # Champ pour le lieu de l'événement, avec une longueur maximale de 255 caractères.

    type_evenement = models.CharField(_('type d\'événement'), max_length=255)
    # Champ pour le type d'événement, avec une longueur maximale de 255 caractères.

    statut = models.CharField(_('statut'), max_length=2, choices=Statut.choices, default=Statut.PLANIFIE)
    # Champ pour le statut de l'événement, avec une longueur maximale de 2 caractères et des choix définis par Statut.

    gestionnaire = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evenements_geres',
        verbose_name=_('gestionnaire'),
        limit_choices_to={'department': 'SUPPORT'},  # Limite la sélection aux utilisateurs du département SUPPORT
    )
    # Clé étrangère vers le modèle Utilisateur. En cas de suppression, le gestionnaire est réglé sur NULL.

    nombre_invites = models.PositiveIntegerField(_('nombre d\'invités'), default=0)
    # Champ pour le nombre d'invités, un entier positif avec 0 comme valeur par défaut.

    note = models.TextField(_('note'), blank=True)
    # Champ pour les notes supplémentaires, facultatif.

    def __str__(self):
        return self.nom
    # Méthode spéciale pour retourner une représentation sous forme de chaîne du modèle.

    @property
    def client_info(self):
        # Propriété pour obtenir les informations du client via le contrat.

        return {
            'client_name': self.contrat.client.nom,
            'client_coordinates': self.contrat.client.coordonnees
        }
        # Renvoie un dictionnaire avec le nom et les coordonnées du client associé au contrat de l'événement.

    @property
    def support_name(self):
        # Propriété pour obtenir le nom du support assigné.

        return self.gestionnaire.nom if self.gestionnaire else None
        # Renvoie le nom du gestionnaire si disponible, sinon None.
