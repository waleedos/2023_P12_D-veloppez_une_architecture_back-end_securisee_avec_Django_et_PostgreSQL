import pytest
from unittest.mock import patch, MagicMock
from user_management import update_user
from epic_auth_app.models import Utilisateur


@pytest.mark.django_db
def test_update_user_success():
    # Créer un faux utilisateur pour le test
    mock_user = MagicMock(spec=Utilisateur)
    mock_user.email = "existing@example.com"

    # Préparer les valeurs simulées pour input()
    inputs = iter(["newemail@example.com", "", "", ""])

    # Assurez-vous que user_to_update est un objet Utilisateur
    with patch('epic_auth_app.models.Utilisateur.objects.get', return_value=mock_user), \
         patch('builtins.input', lambda _: next(inputs)):
        # Mettre à jour les informations de l'utilisateur
        update_user(current_user=mock_user, user_to_update_email=mock_user.email)

        # Vérifier que les informations ont été mises à jour
        assert mock_user.email == "newemail@example.com"
        # Ajoutez les autres assertions si nécessaire


@pytest.mark.django_db
def test_update_user_permission_denied():
    # Créer un faux utilisateur (non superutilisateur et non membre ADM) et un utilisateur cible pour la mise à jour
    mock_current_user = MagicMock(spec=Utilisateur, is_superuser=False, department="COM")
    target_user = MagicMock(spec=Utilisateur, email="target@example.com")

    # Préparer les valeurs simulées pour input()
    inputs = iter(["", "", "", ""])

    with patch('epic_auth_app.models.Utilisateur.objects.get', return_value=target_user), \
         patch('builtins.input', lambda _: next(inputs)):
        # Essayer de mettre à jour les informations de l'utilisateur cible
        update_user(mock_current_user, target_user.email)

        # Vérifier qu'aucune mise à jour n'a été effectuée
        # Ajoutez les assertions appropriées ici
