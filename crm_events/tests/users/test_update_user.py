import pytest
from unittest.mock import patch, MagicMock
from user_management import update_user
from epic_auth_app.models import Utilisateur


@pytest.mark.django_db
def test_update_user_success():
    # Créer un faux utilisateur pour le test
    mock_user = MagicMock(spec=Utilisateur)
    mock_user.email = "existing@example.com"

    # Assurez-vous que user_to_update est un objet Utilisateur
    with patch('epic_auth_app.models.Utilisateur.objects.get', return_value=mock_user):
        # Mettre à jour les informations de l'utilisateur
        update_user(current_user=mock_user, user_to_update_email=mock_user.email,
                    new_email="newemail@example.com",
                    new_first_name="NewFirstName",
                    new_last_name="NewLastName",
                    new_phone="NewPhone")

        # Vérifier que les informations ont été mises à jour
        assert mock_user.email == "newemail@example.com"
        assert mock_user.first_name == "NewFirstName"
        assert mock_user.last_name == "NewLastName"
        assert mock_user.phone == "NewPhone"


@pytest.mark.django_db
def test_update_user_permission_denied():
    # Créer un faux utilisateur (non superutilisateur et non membre ADM) et un utilisateur cible pour la mise à jour
    mock_current_user = MagicMock(spec=Utilisateur, is_superuser=False, department="COM")
    target_user = MagicMock(spec=Utilisateur)

    with patch('epic_auth_app.models.Utilisateur.objects.get', return_value=target_user):
        # Essayer de mettre à jour les informations de l'utilisateur cible
        result = update_user(mock_current_user, "newemail@example.com", "NewFirstName", "NewLastName", "NewPhone")

        # Vérifier qu'aucune mise à jour n'a été effectuée
        assert result is None
        assert target_user.email != "newemail@example.com"
