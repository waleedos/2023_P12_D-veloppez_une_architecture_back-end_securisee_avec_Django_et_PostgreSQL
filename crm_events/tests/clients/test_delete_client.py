import pytest
from unittest.mock import patch
from client_management import delete_client
from epic_clients_app.models import Client
from epic_auth_app.models import Utilisateur


@pytest.fixture
def mock_client_user(db):
    # Créer un utilisateur fictif avec permission (équipe commerciale)
    return Utilisateur.objects.create_user(email="clientuser@example.com", department="COM")


@pytest.fixture
def mock_non_client_user(db):
    # Créer un utilisateur fictif sans permission (département TEST)
    return Utilisateur.objects.create_user(email="nonclientuser@example.com", department="TST")


@pytest.mark.django_db
def test_delete_client_permission(mock_client_user, capfd):
    # Créer un client de test
    client = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone_number="123456789",
        company_name="Test Company"
    )

    # Simuler l'entrée de l'utilisateur pour confirmer la suppression
    with patch('client_management.input', side_effect=[str(client.id), 'yes']):
        delete_client(mock_client_user)

    # Vérifier que le client a été supprimé et que le message approprié est affiché
    with pytest.raises(Client.DoesNotExist):
        Client.objects.get(id=client.id)
    out, err = capfd.readouterr()
    assert "Client deleted successfully." in out


@pytest.mark.django_db
def test_delete_client_no_permission(mock_non_client_user, capfd):
    # Créer un client de test
    client = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone_number="123456789",
        company_name="Test Company"
    )

    # Tenter de supprimer le client sans les permissions nécessaires
    with patch('client_management.input', return_value=str(client.id)):
        delete_client(mock_non_client_user)

    # Vérifier que le client n'a pas été supprimé et que le message de refus d'accès est affiché
    Client.objects.get(id=client.id)
    out, err = capfd.readouterr()
    assert "Accès refusé" in out
