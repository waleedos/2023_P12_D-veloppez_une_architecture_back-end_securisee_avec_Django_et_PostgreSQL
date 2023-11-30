import pytest
from unittest.mock import patch, MagicMock
import user_management
from user_management import create_user


@pytest.mark.django_db
def test_create_user_success(capfd):
    # Simuler un utilisateur connecté avec les permissions requises
    user_management.current_authenticated_user = MagicMock(is_superuser=True, department='ADM')

    # Simuler les entrées de l'utilisateur pour créer un nouvel utilisateur
    with patch(
        'builtins.input',
        side_effect=["nouveau@example.com", "MotDePasse123", "John", "Doe", "0123456789", "COM"]
    ):
        create_user()

    out, err = capfd.readouterr()
    assert "Compte créé pour nouveau@example.com" in out


@pytest.mark.django_db
def test_create_user_permission_denied(capfd):
    # Simuler un utilisateur connecté sans les permissions requises
    user_management.current_authenticated_user = MagicMock(is_superuser=False, department='SUP')

    create_user()
    out, err = capfd.readouterr()
    assert "Vous n'avez pas le niveau d'accréditation ADM pour pouvoir créer un utilisateur." in out


@pytest.mark.django_db
def test_create_user_invalid_input(capfd):
    # Simuler un utilisateur connecté avec les permissions requises
    user_management.current_authenticated_user = MagicMock(is_superuser=True, department='ADM')

    # Simuler les entrées de l'utilisateur avec des valeurs incorrectes
    with patch('builtins.input', side_effect=["invalid_email", "short", "John", "Doe", "0123456789", "COM"]):
        create_user()

    out, err = capfd.readouterr()
    assert "Erreur de validation : " in out
