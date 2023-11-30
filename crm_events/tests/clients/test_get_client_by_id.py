from unittest.mock import patch
from client_management import get_client_by_id
from epic_clients_app.models import Client
import pytest


@pytest.mark.django_db
def test_get_client_by_id():
    # Créer un client de test avec des détails spécifiques
    client = Client.objects.create(
        full_name="Test User",
        email="test@example.com",
        phone_number="1234567890",
        company_name="Test Company"
    )

    # Simuler une entrée utilisateur pour récupérer le client par ID
    with patch('builtins.input', return_value=str(client.id)):
        fetched_client = get_client_by_id()

    # Vérifier que le client récupéré correspond au client créé
    assert fetched_client == client
