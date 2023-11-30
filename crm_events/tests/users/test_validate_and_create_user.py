import pytest
from unittest.mock import patch
from user_management import validate_and_create_user
from epic_auth_app.models import Utilisateur


@pytest.mark.django_db
def test_validate_and_create_user_success(capfd):
    with patch('epic_auth_app.models.Utilisateur.objects.create_user') as mock_create_user:
        mock_create_user.return_value = Utilisateur(email='validemail@example.com')
        validate_and_create_user('validemail@example.com', 'Password123', 'John', 'Doe', '0123456789', 'ADM')
        out, err = capfd.readouterr()
        assert "Compte créé pour validemail@example.com" in out


@pytest.mark.django_db
def test_validate_and_create_user_invalid_email(capfd):
    validate_and_create_user('invalidemail', 'Password123', 'John', 'Doe', '0123456789', 'ADM')
    out, err = capfd.readouterr()
    assert "Erreur de validation : " in out


@pytest.mark.django_db
def test_validate_and_create_user_weak_password(capfd):
    validate_and_create_user('validemail@example.com', '123', 'John', 'Doe', '0123456789', 'ADM')
    out, err = capfd.readouterr()
    assert "Erreur de validation : " in out
