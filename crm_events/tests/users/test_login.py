import pytest
from unittest.mock import patch
from epic_auth_app.models import Utilisateur
from user_management import login


@pytest.mark.django_db
def test_login_success(capfd):
    # Créer un utilisateur de test (ou utiliser un utilisateur existant)
    Utilisateur.objects.create_user(email="testuser@example.com", password="TestPassword")

    login("testuser@example.com", "TestPassword")
    out, err = capfd.readouterr()

    assert "Token JWT généré" in out  # Vérifier la présence de la phrase indiquant qu'un token a été généré


@pytest.mark.django_db
def test_login_failure(capfd):
    with patch('django.contrib.auth.authenticate', return_value=None):
        login("invaliduser@example.com", "WrongPassword")
        out, err = capfd.readouterr()

        assert "Échec de l'authentification pour l'utilisateur" in out
