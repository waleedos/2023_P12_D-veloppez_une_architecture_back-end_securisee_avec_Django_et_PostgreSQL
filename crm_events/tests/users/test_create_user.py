import pytest
from unittest.mock import patch, MagicMock
from user_management import create_user


@pytest.mark.django_db
def test_create_user_success():
    # Mocking l'utilisateur authentifié
    mock_authenticated_user = MagicMock()
    mock_authenticated_user.is_superuser = True

    # Mocking les inputs et les retours attendus
    inputs = iter(["validemail@example.com", "Password123", "John", "Doe", "+1234567890", "ADM"])

    with patch('user_management.current_authenticated_user', mock_authenticated_user), \
         patch('user_management.input_with_prompt', lambda _: next(inputs)), \
         patch('user_management.validate_email'), \
         patch('user_management.validate_password_strength'), \
         patch('user_management.validate_name'), \
         patch('user_management.validate_phone_number'), \
         patch('user_management.Utilisateur.objects.create_user') as mock_create_user:

        create_user()

        # Vérification que la fonction de création d'utilisateur a été appelée
        mock_create_user.assert_called_with(email="validemail@example.com",
                                            password="Password123",
                                            first_name="John",
                                            last_name="Doe",
                                            phone_number="+1234567890",
                                            department="ADM")


@pytest.mark.django_db
def test_create_user_invalid_email():
    # Mocking l'utilisateur authentifié
    mock_authenticated_user = MagicMock()
    mock_authenticated_user.is_superuser = True

    # Préparer les entrées simulées et le retour attendu
    inputs = iter(["invalidemail", "Password123", "John", "Doe", "+1234567890", "ADM"])

    with patch('user_management.current_authenticated_user', mock_authenticated_user), \
         patch('user_management.input_with_prompt', lambda _: next(inputs)), \
         patch('user_management.validate_email') as mock_validate_email:
        mock_validate_email.side_effect = ValueError("Format d'email invalide.")

        create_user()
        mock_validate_email.assert_called_once_with("invalidemail")
