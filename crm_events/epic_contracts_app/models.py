from django.db import models
from django.utils import timezone
from epic_auth_app.models import Utilisateur
from epic_clients_app.models import Client


class Contrat(models.Model):
    # Classe modèle Contrat pour représenter les contrats dans la base de données

    # Définition des choix possibles pour le statut du contrat
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),  # Le contrat est actuellement actif
        ('TERMINE', 'Terminé'),  # Le contrat a été terminé
        ('EN_ATTENTE', 'En attente')  # Le contrat est en attente d'activation ou de traitement
    ]

    # Définition des champs du modèle Contrat
    nom = models.CharField(max_length=25, verbose_name="Nom du contrat", default="Contrat sans nom")
    # Nom du contrat, avec une longueur maximale de 25 caractères et un nom par défaut

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Client')
    # Clé étrangère reliant le contrat à un client spécifique
    # Si le client est supprimé, le contrat associé est également supprimé (CASCADE)

    sales_contact = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Contact commercial',
    )
    # Clé étrangère reliant le contrat à un utilisateur (commercial)
    # Si le commercial est supprimé, la référence dans le contrat est définie sur NULL

    montant_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant total')
    # Champ pour le montant total du contrat, avec une précision de 2 décimales et un maximum de 10 chiffres

    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant restant')
    # Champ pour le montant restant à payer sur le contrat, également avec une précision de 2 décimales

    date_creation = models.DateTimeField(default=timezone.now, verbose_name='Date de création')
    # Date et heure de création du contrat, par défaut à la date et heure actuelle

    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='EN_ATTENTE', verbose_name='Statut')
    # Champ pour le statut du contrat, avec des valeurs prédéfinies et un statut par défaut 'En attente'

    def __str__(self):
        # Méthode pour la représentation en chaîne de caractères du contrat
        return f"{self.nom} (ID: {self.id}) - Client: {self.client.full_name}"
        # Retourne une chaîne formatée avec le nom du contrat, son ID et le nom complet du client associé
