import pytest
from unittest.mock import patch, MagicMock
from epic_auth_app.models import Utilisateur
from epic_clients_app.models import Client
from client_management import add_client


@pytest.fixture
def mock_current_user():
    return MagicMock(spec=Utilisateur, email="testuser@example.com", department="COM")


@pytest.mark.django_db
def test_add_client_success():
    test_user = Utilisateur.objects.create(email="testuser@example.com", department="COM")

    # Utilisez un numéro de téléphone valide
    client_data = ["John Doe", "john@example.com", "+12345678901", "Doe Inc."]

    with patch('client_management.input', side_effect=client_data):
        with patch('client_management.is_valid_email', return_value=True):
            add_client(test_user)

            added_client = Client.objects.filter(email="john@example.com").first()
            assert added_client is not None
            assert added_client.full_name == "John Doe"
            assert added_client.phone_number == "+12345678901"
            assert added_client.company_name == "Doe Inc."


@pytest.mark.django_db
def test_add_client_access_denied(mock_current_user):
    # Modifier le département de l'utilisateur mocké pour simuler un accès refusé
    mock_current_user.department = "AUTRE"

    with patch('client_management.input', side_effect=["Jane Doe", "jane@example.com", "987654321", "Doe Enterprises"]):
        with patch('client_management.is_valid_email', return_value=True):
            with patch('builtins.print') as mock_print:
                # Appeler la fonction add_client avec l'utilisateur mocké
                add_client(mock_current_user)

                # Vérifier que le bon message a été imprimé
                expected_msg = ("\n\033[91mAccès refusé. Seuls les membres de l'équipe commerciale "
                                "peuvent ajouter des clients.\033[0m")
                mock_print.assert_called_with(expected_msg)
