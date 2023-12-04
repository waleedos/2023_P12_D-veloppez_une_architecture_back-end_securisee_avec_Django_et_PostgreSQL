from django.test import TestCase
from epic_auth_app.models import Utilisateur
from epic_events_app.models import Evenement
from epic_contracts_app.models import Contrat
from epic_clients_app.models import Client
from datetime import timedelta
from unittest.mock import patch
from io import StringIO
from django.utils import timezone
from event_management import list_events


class ListEventsTest(TestCase):
    def setUp(self):
        # Création des utilisateurs
        self.user_ges = Utilisateur.objects.create_user(email='ges@example.com', password='testpass', department='GES')
        self.user_adm = Utilisateur.objects.create_user(email='adm@example.com', password='testpass', department='ADM')
        self.user_com = Utilisateur.objects.create_user(email='com@example.com', password='testpass', department='COM')
        self.user_sup = Utilisateur.objects.create_user(email='sup@example.com', password='testpass', department='SUP')

        # Création d'un client
        self.client = Client.objects.create(
            full_name='Client Test',
            email='client@example.com',
            phone_number='0123456789',
            company_name='Entreprise Test',
            sales_contact=self.user_com
        )

        # Création d'un contrat
        self.contrat = Contrat.objects.create(
            nom='Contrat Test',
            montant_total=1000,
            montant_restant=500,
            date_creation=timezone.now(),
            statut='ACTIF',
            client=self.client
        )

        # Création des événements
        self.event1 = Evenement.objects.create(
            nom='Événement 1',
            date_debut=timezone.now(),
            date_fin=timezone.now() + timedelta(days=1),
            lieu='Lieu 1',
            type_evenement='Type 1',
            statut='PL',
            contrat=self.contrat,
            gestionnaire=self.user_sup
        )
        self.event2 = Evenement.objects.create(
            nom='Événement 2',
            date_debut=timezone.now(),
            date_fin=timezone.now() + timedelta(days=2),
            lieu='Lieu 2',
            type_evenement='Type 2',
            statut='PL',
            contrat=self.contrat,
            gestionnaire=self.user_adm
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_events_for_ges(self, mock_stdout):
        list_events(self.user_ges)
        output = mock_stdout.getvalue()
        self.assertIn("Événement 1", output)
        self.assertIn("Événement 2", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_events_for_adm(self, mock_stdout):
        list_events(self.user_adm)
        output = mock_stdout.getvalue()
        self.assertIn("Événement 1", output)
        self.assertIn("Événement 2", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_events_for_com(self, mock_stdout):
        list_events(self.user_com)
        output = mock_stdout.getvalue()
        self.assertIn("Événement 1", output)
        self.assertIn("Événement 2", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_events_for_sup(self, mock_stdout):
        # Ce test doit être ajusté pour vérifier que seuls les événements attribués au gestionnaire SUP sont listés
        list_events(self.user_sup)
        output = mock_stdout.getvalue()
        self.assertIn("Événement 1", output)  # Assumant que l'événement 1 est attribué à user_sup
        self.assertNotIn("Événement 2", output)  # Assumant que l'événement 2 n'est pas attribué à user_sup

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_events_for_user_without_permission(self, mock_stdout):
        # Ce test doit vérifier que l'utilisateur reçoit un message d'accès refusé
        user_tech = Utilisateur.objects.create_user(email='tech@example.com', password='testpass', department='TEC')
        list_events(user_tech)
        output = mock_stdout.getvalue()
        self.assertIn("Accès refusé. Vous n'avez pas l'autorisation nécessaire", output)
