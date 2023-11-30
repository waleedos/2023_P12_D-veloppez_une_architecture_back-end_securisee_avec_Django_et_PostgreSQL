from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from epic_auth_app.models import Utilisateur


# Modèle Client
class Client(models.Model):
    # Enumération pour les rôles
    class Role(models.TextChoices):
        PROSPECT = 'PR', _('Prospect')
        CLIENT = 'CL', _('Client')

    full_name = models.CharField(_('nom complet'), max_length=255)
    email = models.EmailField(_('email'), unique=True)
    phone_number = models.CharField(_('téléphone'), max_length=20)
    company_name = models.CharField(_('nom de l’entreprise'), max_length=255)
    created_at = models.DateTimeField(_('date de création'), default=timezone.now)
    updated_at = models.DateTimeField(_('dernière mise à jour'), auto_now=True)
    sales_contact = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients',
        verbose_name=_('contact commercial chez Epic Events')
    )
    role = models.CharField(_('rôle'), max_length=2, choices=Role.choices, default=Role.PROSPECT)

    def __str__(self):
        return self.full_name
