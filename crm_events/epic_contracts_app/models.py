from django.db import models
from django.utils import timezone
from epic_auth_app.models import Utilisateur
from epic_clients_app.models import Client


class Contrat(models.Model):
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('TERMINE', 'Terminé'),
        ('EN_ATTENTE', 'En attente')
    ]

    nom = models.CharField(max_length=25, verbose_name="Nom du contrat", default="Contrat sans nom")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Client')
    sales_contact = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Contact commercial',
    )
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant total')
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant restant')
    date_creation = models.DateTimeField(default=timezone.now, verbose_name='Date de création')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='EN_ATTENTE', verbose_name='Statut')

    def __str__(self):
        return f"{self.nom} (ID: {self.id}) - Client: {self.client.full_name}"
