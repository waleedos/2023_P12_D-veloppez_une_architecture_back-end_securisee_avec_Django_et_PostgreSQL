import pytest
from user_management import get_current_user, login
from epic_auth_app.models import Utilisateur


@pytest.mark.django_db
def test_get_current_user():
    # Créer un utilisateur de test
    test_email = "testuser@example.com"
    test_password = "TestPassword123"
    Utilisateur.objects.create_user(email=test_email, password=test_password)

    # Simuler une connexion pour définir l'utilisateur actuel
    login(test_email, test_password)

    # Appeler get_current_user
    current_user = get_current_user()

    # Vérifier que get_current_user renvoie bien l'utilisateur connecté
    assert current_user is not None
    assert current_user.email == test_email
