import pytest
from django.core.exceptions import ValidationError
from user_management import validate_password_strength


def test_validate_password_strength_valid():
    # Test avec un mot de passe valide
    try:
        validate_password_strength("ValidPassword123")
        assert True  # Le mot de passe est valide, donc pas d'exception levée
    except ValidationError:
        assert False  # Si une exception est levée, le test échoue


def test_validate_password_strength_invalid():
    # Test avec un mot de passe invalide
    with pytest.raises(ValidationError):
        validate_password_strength("weak")
