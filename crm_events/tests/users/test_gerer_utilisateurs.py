import pytest
from unittest.mock import patch, MagicMock
from user_management import gerer_utilisateurs
from epic_auth_app.models import Utilisateur


@pytest.mark.django_db
def test_gerer_utilisateurs(capfd):
    # Création d'un utilisateur de test dans la base de données
    Utilisateur.objects.create_user(
        email="testuser@example.com",
        password="password123",
        first_name="Test",
        last_name="User",
        department="ADM"
    )

    # Simuler un utilisateur connecté
    current_authenticated_user = MagicMock(
        email="testuser@example.com",
        department="ADM",
        is_superuser=True
    )

    # Simuler les entrées de l'utilisateur pour différentes actions
    with patch('builtins.input', side_effect=["1", "6", "ADM", "7"]):  # "1" pour afficher, "6" pour filtrer, "ADM" pour le code de département, "7" pour quitter
        gerer_utilisateurs(current_authenticated_user)

    # Capturer la sortie
    out, _ = capfd.readouterr()

    # Vérifier les sorties attendues
    assert "Gestion des Utilisateurs" in out
    assert "Afficher tous les Utilisateurs" in out
    assert "Créer un nouvel Utilisateur" in out
    assert "Supprimer un Utilisateur" in out
    assert "Réaffecter un Utilisateur" in out
    assert "Mettre à jour un Utilisateur" in out
    assert "Filtrer les utilisateurs par Département" in out
    assert "Revenir au menu précédent" in out
    assert "testuser@example.com" in out  # Vérifie que la liste des utilisateurs s'affiche
