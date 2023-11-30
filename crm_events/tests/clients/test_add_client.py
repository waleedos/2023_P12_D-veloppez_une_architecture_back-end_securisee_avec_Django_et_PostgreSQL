import pytest
from unittest.mock import patch, MagicMock
from client_management import add_client
from epic_clients_app.models import Client


@pytest.fixture
def mock_client_user():
    return MagicMock(department='COM')


@pytest.fixture
def mock_non_client_user():
    return MagicMock(department='SUP')


@pytest.mark.django_db
def test_add_client_success(mock_client_user):
    with patch('client_management.input', side_effect=["John Doe", "john@example.com", "123456789", "Doe Inc."]):
        with patch('client_management.is_valid_email', return_value=True):
            add_client(mock_client_user)
            assert Client.objects.filter(email="john@example.com").exists()


@pytest.mark.django_db
def test_add_client_access_denied(mock_non_client_user):
    with patch('client_management.input', side_effect=["Jane Doe", "jane@example.com", "987654321", "Doe Enterprises"]):
        with patch('client_management.is_valid_email', return_value=True):
            add_client(mock_non_client_user)
            assert not Client.objects.filter(email="jane@example.com").exists()
