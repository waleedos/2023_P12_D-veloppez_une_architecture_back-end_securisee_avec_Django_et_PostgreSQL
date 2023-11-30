from django.test import TestCase
from epic_auth_app.models import Utilisateur
from epic_events_app.models import Evenement
from epic_contracts_app.models import Contrat
from epic_clients_app.models import Client
from datetime import timedelta
from django.utils import timezone


class TestEventCreation(TestCase):
    def setUp(self):
        # Création des utilisateurs de test
        self.user_ges = Utilisateur.objects.create_user(
            email='ges@example.com', password='testpass', department='GES')

        self.user_adm = Utilisateur.objects.create_user(
            email='adm@example.com', password='testpass', department='ADM')

        self.user_com = Utilisateur.objects.create_user(
            email='com@example.com', password='testpass', department='COM')

        self.user_sup = Utilisateur.objects.create_user(
            email='sup@example.com', password='testpass', department='SUP')
        # Ajoutez d'autres utilisateurs au besoin

        # Création de clients de test
        self.client_test = Client.objects.create(
            full_name='Nom Complet Client',
            email='client@example.com',
            phone_number='0123456789',
            company_name='Nom de l’Entreprise',
            sales_contact=self.user_com,
            role=Client.Role.CLIENT
        )

        # Création de contrats de test
        self.contrat1 = Contrat.objects.create(
            nom='Contrat Test 1',
            montant_total=1000,
            montant_restant=500,
            date_creation=timezone.now(),
            statut='ACTIF',
            client=self.client_test
        )
        # Ajoutez d'autres contrats au besoin

        # Création des événements de test
        self.event1 = Evenement.objects.create(
            nom='Événement 1',
            date_debut=timezone.now(),
            date_fin=timezone.now() + timedelta(days=1),
            lieu='Lieu 1',
            type_evenement='Type 1',
            statut=Evenement.Statut.PLANIFIE,
            contrat=self.contrat1,
            gestionnaire=self.user_ges
        )
        self.event2 = Evenement.objects.create(
            nom='Événement 2',
            date_debut=timezone.now(),
            date_fin=timezone.now() + timedelta(days=2),
            lieu='Lieu 2',
            type_evenement='Type 2',
            statut=Evenement.Statut.PLANIFIE,
            contrat=self.contrat1,
            gestionnaire=self.user_adm
        )

        # Impression des événements pour confirmation
        print("Événements créés pour les tests :")
        for event in Evenement.objects.all():
            print(f"{event.nom}, Géré par : {event.gestionnaire.email if event.gestionnaire else 'N/A'}")

    def test_event_creation(self):
        # Vérification de la création des événements
        event1 = Evenement.objects.get(nom='Événement 1')
        self.assertEqual(event1.nom, 'Événement 1')
        self.assertEqual(event1.gestionnaire, self.user_ges)
        self.assertEqual(event1.contrat, self.contrat1)

        # Test pour event2
        event2 = Evenement.objects.get(nom='Événement 2')
        self.assertEqual(event2.nom, 'Événement 2')
        self.assertEqual(event2.gestionnaire, self.user_adm)
        self.assertEqual(event2.contrat, self.contrat1)
