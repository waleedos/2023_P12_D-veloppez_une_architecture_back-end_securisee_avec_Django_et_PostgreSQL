import pytest
from user_management import list_users
from epic_auth_app.models import Utilisateur


@pytest.mark.django_db
def test_list_users(capfd):
    # Création d'utilisateurs de test
    Utilisateur.objects.create_user(
        email="user1@example.com", password="Password1", first_name="User", last_name="One", department="COM")
    Utilisateur.objects.create_user(
        email="user2@example.com", password="Password2", first_name="User", last_name="Two", department="SUP")

    # Appel de la fonction list_users()
    list_users()
    out, err = capfd.readouterr()

    # Vérifier que tous les utilisateurs et les en-têtes sont listés
    assert "user1@example.com" in out
    assert "user2@example.com" in out
    assert " Email " in out
    assert " First Name " in out
    assert " Last Name " in out
    assert " Department " in out
    assert " Is Superuser " in out

    # Vérifier le formatage de la sortie avec les bordures bleues personnalisées
    assert '\033[94m╔' in out  # Début de la bordure du tableau
    assert '\033[94m║' in out  # Début d'une ligne du tableau
    assert '\033[94m╚' in out  # Fin de la bordure du tableau

    # Vérifier la présence de la ligne séparatrice après les en-têtes
    assert '╠' in out or '╣' in out  # Séparateur de tableau, par exemple

    # Vérifier que la sortie contient les lignes pour chaque utilisateur
    lines = out.split('\n')
    assert any("user1@example.com" in line for line in lines)
    assert any("user2@example.com" in line for line in lines)
