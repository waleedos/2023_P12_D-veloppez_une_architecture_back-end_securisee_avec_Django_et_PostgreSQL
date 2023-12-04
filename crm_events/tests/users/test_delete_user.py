import pytest
from unittest.mock import MagicMock, patch
from user_management import delete_user
from epic_auth_app.models import Utilisateur


# Test de succès
@pytest.mark.django_db
def test_delete_user_success():
    # Créer des faux utilisateurs pour le test
    mock_requesting_user = MagicMock(spec=Utilisateur, is_superuser=True)
    mock_user_to_delete = MagicMock(spec=Utilisateur, email="user@example.com")

    with patch('epic_auth_app.models.Utilisateur.objects.get', side_effect=[mock_requesting_user, mock_user_to_delete]):
        # Configurer le mock pour la méthode delete directement sur l'instance mock_user_to_delete
        mock_user_to_delete.delete = MagicMock()

        delete_user("superuser@example.com", "user@example.com")
        mock_user_to_delete.delete.assert_called_once()


@pytest.mark.django_db
def test_delete_user_permission_denied(capfd):
    # Créer des faux utilisateurs pour le test
    mock_requesting_user = MagicMock(spec=Utilisateur, is_superuser=False, department="COM")
    mock_user_to_delete = MagicMock(spec=Utilisateur, email="user@example.com")

    with patch('epic_auth_app.models.Utilisateur.objects.get', side_effect=[mock_requesting_user, mock_user_to_delete]):
        delete_user("nonadminuser@example.com", "user@example.com")
        captured = capfd.readouterr()
        assert "\033[91mVous n'avez pas le niveau d'accréditation (ADM ou GES), nécessaire pour supprimer cet utilisateur.\n" in captured.out
