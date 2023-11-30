from unittest.mock import patch
from django.test import TestCase
from contract_management import gerer_contrats
from epic_auth_app.models import Utilisateur


class GererContratsTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(email='test@example.com', password='testpass123', department='GES')

    @patch('builtins.input', side_effect=['1', '6'])  # Choix pour lister les contrats puis quitter
    @patch('contract_management.list_contrats')
    def test_redirect_to_list_contrats(self, mock_list_contrats, mock_input):
        gerer_contrats(self.user)
        mock_list_contrats.assert_called_once_with(self.user)

    @patch('builtins.input', side_effect=['2', '6'])  # Choix pour créer un contrat puis quitter
    @patch('contract_management.create_contrat')
    def test_redirect_to_create_contrat(self, mock_create_contrat, mock_input):
        gerer_contrats(self.user)
        mock_create_contrat.assert_called_once_with(self.user)

    @patch('builtins.input', side_effect=['3', '1', '6'])  # Choix pour modifier un contrat puis quitter
    @patch('contract_management.update_contrat')
    def test_redirect_to_update_contrat(self, mock_update_contrat, mock_input):
        gerer_contrats(self.user)
        mock_update_contrat.assert_called_once_with(self.user, '1')

    @patch('builtins.input', side_effect=['4', '1', '6'])  # Choix pour supprimer un contrat puis quitter
    @patch('contract_management.delete_contrat')
    def test_redirect_to_delete_contrat(self, mock_delete_contrat, mock_input):
        gerer_contrats(self.user)
        mock_delete_contrat.assert_called_once_with(self.user, '1')

    @patch('builtins.input', side_effect=['5', '1', '6'])  # Choix pour réaffecter un contrat puis quitter
    @patch('contract_management.reassign_contrat')
    def test_redirect_to_reassign_contrat(self, mock_reassign_contrat, mock_input):
        gerer_contrats(self.user)
        mock_reassign_contrat.assert_called_once_with(self.user, '1')
