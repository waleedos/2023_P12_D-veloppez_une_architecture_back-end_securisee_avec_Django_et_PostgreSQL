from client_management import is_valid_email


def test_is_valid_email():
    valid_email = "test@example.com"
    invalid_email = "test@example"

    # Utilisez 'is True' pour la comparaison
    assert is_valid_email(valid_email) is True
    # Utilisez 'is False' pour la comparaison
    assert is_valid_email(invalid_email) is False
