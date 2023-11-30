import unittest
from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone
from epic_auth_app.models import Utilisateur
from epic_contracts_app.models import Contrat
from epic_clients_app.models import Client
from contract_management import list_contrats


class TestListContracts(TestCase):

    def setUp(self):
        # Création d'utilisateurs de test pour différents départements
        self.user_ges = Utilisateur.objects.create_user(
            email='ges@example.com', password='testpass123', department='GES')
        self.client1 = Client.objects.create(
            full_name='Client 1', email='client1@example.com',
            phone_number='123456789', company_name='Test Company')
        self.client2 = Client.objects.create(
            full_name='Client 2', email='client2@example.com',
            phone_number='987654321', company_name='Test Company')

    @patch('contract_management.print')
    def test_list_contrats_correct_headers_and_data(self, mock_print):
        # Création des contrats de test
        Contrat.objects.create(
            nom='Contrat 1', client=self.client1, sales_contact=self.user_ges,
            montant_total=1000, montant_restant=500,
            date_creation=timezone.now(), statut='ACTIF')
        Contrat.objects.create(
            nom='Contrat 2', client=self.client2, sales_contact=self.user_ges,
            montant_total=2000, montant_restant=1000,
            date_creation=timezone.now(), statut='TERMINE')

        list_contrats(self.user_ges)

        # Vérifiez que les en-têtes et les données attendues sont dans la sortie
        expected_headers = ('\x1b[38;5;202m║ ID   Nom          Client      Montant Total  '
                            'Montant Restant  Date de Création    Statut     '
                            'Géré par (Dpt Gestion)     ║\x1b[0m')
        actual_output = [call_args[0][0] for call_args in mock_print.call_args_list]
        self.assertIn(expected_headers, actual_output)


if __name__ == '__main__':
    unittest.main()
