from django.test import TestCase
from epic_auth_app.models import Utilisateur
from epic_contracts_app.models import Contrat, Client
from contract_management import reassign_contrat
from django.utils import timezone
from unittest.mock import patch


class ReassignContratTest(TestCase):

    def setUp(self):
        self.user_ges = Utilisateur.objects.create_user(email='ges@example.com', password='testpass123', department='GES')
        self.user_adm = Utilisateur.objects.create_user(email='adm@example.com', password='testpass123', department='ADM')
        self.user_tst = Utilisateur.objects.create_user(email='tst@example.com', password='testpass123', department='TST')
        self.new_sales_contact = Utilisateur.objects.create_user(
            email='new_sales@example.com', password='testpass123', department='COM'
        )
        self.client_test = Client.objects.create(full_name='Test Client', email='client@example.com')
        self.contrat_test = Contrat.objects.create(
            nom='Test Contract', client=self.client_test, sales_contact=self.user_ges,
            montant_total=1000, montant_restant=500, date_creation=timezone.now(),
            statut='ACTIF')

    def test_reassign_contrat_success(self):
        with patch('builtins.input', return_value='new_sales@example.com'):
            reassign_contrat(self.user_adm, self.contrat_test.id)
            reassigned_contrat = Contrat.objects.get(id=self.contrat_test.id)
            self.assertEqual(reassigned_contrat.sales_contact, self.new_sales_contact)

    def test_refusal_for_non_authorized_users(self):
        with patch('builtins.print') as mock_print:
            reassign_contrat(self.user_tst, self.contrat_test.id)
            expected_message = ("\033[91mSeules les personnes appartenant aux équipes "
                                "de gestion et administration peuvent réaffecter un contrat.\033[0m")
            mock_print.assert_called_with(expected_message)

    def test_contract_or_new_sales_contact_not_found(self):
        with patch('builtins.print') as mock_print:
            # Test with non-existent contract ID
            reassign_contrat(self.user_adm, 999)
            mock_print.assert_called_with("\033[91mContrat non trouvé.\033[0m")

            # Reset mock for next assertion
            mock_print.reset_mock()

            # Test with non-existent new sales contact
            with patch('builtins.input', return_value='non_existent@example.com'):
                reassign_contrat(self.user_adm, self.contrat_test.id)
                mock_print.assert_called_with("\033[91mUtilisateur non trouvé.\033[0m")
