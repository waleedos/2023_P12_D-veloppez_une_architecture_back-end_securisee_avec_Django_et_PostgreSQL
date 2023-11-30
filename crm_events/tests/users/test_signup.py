import pytest
from user_management import signup
from epic_auth_app.models import Utilisateur
from unittest.mock import patch


@pytest.mark.django_db
def test_signup_success():
    # Données de l'utilisateur à créer
    new_user_data = {
        "email": "newuser@example.com",
        "password": "NewPassword123",
        "first_name": "New",
        "last_name": "User",
        "department": "COM"
    }

    with patch('user_management.input', side_effect=[new_user_data["email"],
                                                     new_user_data["password"],
                                                     new_user_data["first_name"],
                                                     new_user_data["last_name"],
                                                     new_user_data["department"]]):
        signup()

    # Vérifier si l'utilisateur a été créé
    created_user = Utilisateur.objects.get(email=new_user_data["email"])
    assert created_user is not None
    assert created_user.first_name == new_user_data["first_name"]
    assert created_user.last_name == new_user_data["last_name"]
    assert created_user.department == new_user_data["department"]


@pytest.mark.django_db
def test_signup_failure_invalid_email(capfd):
    # Données de l'utilisateur avec un email invalide
    invalid_user_data = {
        "email": "invalidemail",
        "password": "Password123",
        "first_name": "Invalid",
        "last_name": "Email",
        "department": "COM"
    }

    with patch('user_management.input', side_effect=[invalid_user_data["email"],
                                                     invalid_user_data["password"],
                                                     invalid_user_data["first_name"],
                                                     invalid_user_data["last_name"],
                                                     invalid_user_data["department"]]):
        signup()

        out, _ = capfd.readouterr()  # Capture la sortie de la fonction signup
        assert "Format d'email invalide." in out  # Vérifiez si le message d'erreur est imprimé
