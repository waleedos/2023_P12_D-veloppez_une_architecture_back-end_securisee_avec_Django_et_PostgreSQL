import pytest
from client_management import list_clients
from epic_clients_app.models import Client


@pytest.mark.django_db
def test_list_clients(capfd):
    # Créer des clients de test avec des détails spécifiques
    Client.objects.create(
        full_name="Client A",
        email="clienta@example.com",
        phone_number="1234567890",
        company_name="Company A",
    )

    Client.objects.create(
        full_name="Client B",
        email="clientb@example.com",
        phone_number="0987654321",
        company_name="Company B",
    )

    # Appeler list_clients
    list_clients()

    # Capturer la sortie imprimée
    out, err = capfd.readouterr()

    # Vérifier que la sortie imprimée contient les informations des clients créés
    assert "Client A" in out
    assert "clienta@example.com" in out
    assert "Client B" in out
    assert "clientb@example.com" in out
