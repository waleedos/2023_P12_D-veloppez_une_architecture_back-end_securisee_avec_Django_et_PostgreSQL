from django.test import TestCase
from django.contrib.auth import get_user_model
from epic_auth_app.models import Utilisateur
from epic_clients_app.models import Client
from contract_management import create_contrat
from unittest.mock import patch
from io import StringIO


User = get_user_model()


class ContractManagementTest(TestCase):

    def setUp(self):
        # Création d'un utilisateur autorisé
        self.user_ges = Utilisateur.objects.create_user(
            email="ges@example.com", password="test", department="GES"
        )
        self.user_adm = Utilisateur.objects.create_user(
            email="adm@example.com", password="test", department="ADM"
        )

        # Création d'un utilisateur non autorisé
        self.user_other = Utilisateur.objects.create_user(
            email="other@example.com", password="test", department="COM"
        )

        # Création d'un client de test
        self.client = Client.objects.create(
            full_name="Test Client",
            email="client@example.com",
            phone_number="1234567890",
            company_name="Test Company",
        )

    def test_create_contrat_not_allowed(self):
        # Test pour un utilisateur non autorisé
        with patch("sys.stdout", new=StringIO()) as fake_output:
            create_contrat(self.user_other)
            self.assertIn(
                "Seuls les membres des équipes de gestion ou d'administration peuvent créer des contrats",
                fake_output.getvalue(),
            )

    def test_create_contrat_client_not_found(self):
        # Test pour un client inexistant
        with patch("builtins.input", side_effect=["Test Contract", "999", "1000", "500", "2023-05-01 10:00", "ACT"]):
            with patch("sys.stdout", new=StringIO()) as fake_output:
                create_contrat(self.user_ges)
                self.assertIn("Client introuvable", fake_output.getvalue())
