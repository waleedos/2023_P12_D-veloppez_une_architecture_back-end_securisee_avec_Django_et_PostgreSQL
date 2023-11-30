from django.test import TestCase
from epic_auth_app.models import Utilisateur
from epic_contracts_app.models import Contrat, Client
from contract_management import update_contrat
from django.utils import timezone
from unittest.mock import patch


class UpdateContratTest(TestCase):

    def setUp(self):
        self.user_ges = Utilisateur.objects.create_user(
            email='ges@example.com', password='testpass123', department='GES')
        self.user_adm = Utilisateur.objects.create_user(
            email='adm@example.com', password='testpass123', department='ADM')
        self.user_tst = Utilisateur.objects.create_user(
            email='tst@example.com', password='testpass123', department='TST')
        self.client_test = Client.objects.create(
            full_name='Test Client', email='client@example.com')
        self.contrat_test = Contrat.objects.create(
            nom='Test Contract', client=self.client_test,
            sales_contact=self.user_ges, montant_total=1000,
            montant_restant=500, date_creation=timezone.now(),
            statut='ACTIF')

    def test_update_contrat_success(self):
        with patch('builtins.input', side_effect=['Updated Contract', '1200', '600', 'ACT']):
            update_contrat(self.user_ges, self.contrat_test.id)
            updated_contrat = Contrat.objects.get(id=self.contrat_test.id)
            self.assertEqual(updated_contrat.nom, 'Updated Contract')
            self.assertEqual(updated_contrat.montant_total, 1200)
            self.assertEqual(updated_contrat.montant_restant, 600)
            self.assertEqual(updated_contrat.statut, 'ACTIF')

    def test_refusal_for_non_authorized_users(self):
        with patch('builtins.print') as mock_print:
            update_contrat(self.user_tst, self.contrat_test.id)
            expected_message = ("\033[91mSeuls les membres des équipes de gestion "
                                "et administration peuvent modifier un contrat.\033[0m")
            mock_print.assert_called_with(expected_message)

    def test_contract_not_found(self):
        with patch('builtins.print') as mock_print:
            update_contrat(self.user_ges, 999)  # ID inexistant
            mock_print.assert_called_with("\033[91mContrat non trouvé.\033[0m")
