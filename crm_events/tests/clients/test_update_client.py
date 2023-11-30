import pytest
from unittest.mock import patch
from client_management import update_client
from epic_clients_app.models import Client
from epic_auth_app.models import Utilisateur


@pytest.fixture
def mock_client_user(db):
    # Créer un utilisateur fictif avec permission (équipe commerciale)
    return Utilisateur.objects.create_user(email="clientuser@example.com", department="COM")


@pytest.fixture
def mock_non_client_user(db):
    return Utilisateur.objects.create_user(email="nonclientuser@example.com", department="TST")


@pytest.mark.django_db
def test_update_client_permission(mock_client_user):
    client = Client.objects.create(
        full_name="John Doe",
        email="john@example.com",
        phone_number="123456789",
        company_name="Doe Inc."
    )

    new_data = ["Jane Doe", "jane@example.com", "987654321", "Doe Enterprises"]

    with patch('client_management.get_client_by_id', return_value=client):
        with patch('client_management.input', side_effect=new_data):
            with patch('client_management.is_valid_email', return_value=True):
                update_client(mock_client_user)

    updated_client = Client.objects.get(id=client.id)
    assert updated_client.full_name == "Jane Doe"
    assert updated_client.email == "jane@example.com"
    assert updated_client.phone_number == "987654321"
    assert updated_client.company_name == "Doe Enterprises"


@pytest.mark.django_db
def test_update_client_no_permission(mock_non_client_user, capfd):
    client = Client.objects.create(
        full_name="John Doe",
        email="john@example.com",
        phone_number="123456789",
        company_name="Doe Inc."
    )

    with patch('client_management.get_client_by_id', return_value=client):
        with patch('client_management.input', side_effect=[
            "Jane Doe",
            "jane@example.com",
        ]):
            with patch('client_management.input', side_effect=[
                "987654321",
                "Doe Enterprises",
            ]):
                update_client(mock_non_client_user)

    out, err = capfd.readouterr()
    unchanged_client = Client.objects.get(id=client.id)

    assert unchanged_client.full_name == "John Doe"
    assert "Accès refusé" in out
