from django.test import TestCase
from epic_auth_app.models import Utilisateur
from epic_contracts_app.models import Contrat, Client
from contract_management import delete_contrat
from django.utils import timezone
from unittest.mock import patch


class DeleteContratTest(TestCase):

    def setUp(self):
        # Création d'utilisateurs de différents départements
        self.user_ges = Utilisateur.objects.create_user(email='ges@example.com', password='testpass123', department='GES')
        self.user_adm = Utilisateur.objects.create_user(email='adm@example.com', password='testpass123', department='ADM')
        self.user_tst = Utilisateur.objects.create_user(email='tst@example.com', password='testpass123', department='TST')

        # Création d'un client test
        self.client_test = Client.objects.create(full_name='Test Client', email='client@example.com')

        # Création d'un contrat test associé à l'utilisateur 'user_ges' et au 'client_test'
        self.contrat_test = Contrat.objects.create(
            nom='Test Contract',
            client=self.client_test,
            sales_contact=self.user_ges,
            montant_total=1000,
            montant_restant=500,
            date_creation=timezone.now(),
            statut='ACTIF')

    def test_delete_contrat_success(self):
        with patch('builtins.input', return_value='oui'):
            delete_contrat(self.user_adm, self.contrat_test.id)
            self.assertFalse(Contrat.objects.filter(id=self.contrat_test.id).exists())

    def test_refusal_for_non_authorized_users(self):
        with patch('builtins.input', return_value='non'), \
                patch('builtins.print') as mock_print:
            # Utiliser un utilisateur non autorisé, par exemple 'user_tst'
            delete_contrat(self.user_tst, self.contrat_test.id)

            expected_message = ("\033[91mSeules les personnes appartenant aux "
                                "équipes de gestion et administration peuvent "
                                "supprimer un contrat.\033[0m")
            mock_print.assert_called_with(expected_message)

    def test_contract_not_found(self):
        with patch('builtins.print') as mock_print:
            delete_contrat(self.user_adm, 999)  # ID inexistant
            mock_print.assert_called_with("\033[91mContrat non trouvé.\033[0m")
