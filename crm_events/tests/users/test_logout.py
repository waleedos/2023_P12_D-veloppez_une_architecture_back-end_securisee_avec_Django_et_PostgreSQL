import pytest
from user_management import login, logout, get_current_user
from epic_auth_app.models import Utilisateur


@pytest.mark.django_db
def test_logout():
    # Créer et connecter un utilisateur de test
    test_email = "testlogout@example.com"
    test_password = "TestPassword123"
    Utilisateur.objects.create_user(email=test_email, password=test_password)
    login(test_email, test_password)

    # Vérifier qu'un utilisateur est actuellement connecté
    assert get_current_user() is not None

    # Appeler logout
    logout()

    # Vérifier qu'aucun utilisateur n'est actuellement connecté
    assert get_current_user() is None
