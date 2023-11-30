from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from epic_contracts_app.models import Contrat
from epic_auth_app.models import Utilisateur


class Evenement(models.Model):
    class Statut(models.TextChoices):
        PLANIFIE = 'PL', _('Planifié')
        REALISE = 'RE', _('Réalisé')
        ANNULE = 'AN', _('Annulé')

    nom = models.CharField(_('nom'), max_length=255)
    date_debut = models.DateTimeField(_('date de début'), default=timezone.now)
    date_fin = models.DateTimeField(_('date de fin'), default=timezone.now)
    lieu = models.CharField(_('lieu'), max_length=255)
    type_evenement = models.CharField(_('type d\'événement'), max_length=255)
    statut = models.CharField(_('statut'), max_length=2, choices=Statut.choices, default=Statut.PLANIFIE)
    contrat = models.ForeignKey(
        Contrat,
        on_delete=models.CASCADE,
        related_name='evenements',
        verbose_name=_('contrat associé'),
    )

    gestionnaire = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evenements_geres',
        verbose_name=_('gestionnaire'),
    )

    def __str__(self):
        return self.nom
