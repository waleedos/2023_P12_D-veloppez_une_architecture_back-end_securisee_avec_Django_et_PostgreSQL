import pytest
from user_management import reassign_user
from epic_auth_app.models import Utilisateur


@pytest.mark.django_db
def test_reassign_user():
    # Créer un superutilisateur et un utilisateur normal pour le test
    superuser = Utilisateur.objects.create_superuser(
        email="superuser@example.com",
        password="SuperPassword"
    )
    normal_user = Utilisateur.objects.create_user(
        email="normaluser@example.com",
        password="NormalPassword",
        department="COM"
    )

    # Réaffecter l'utilisateur normal à un nouveau département par le superutilisateur
    new_department = "ADM"
    reassign_user(normal_user.email, new_department, superuser.email)

    # Récupérer l'utilisateur mis à jour de la base de données
    updated_user = Utilisateur.objects.get(email=normal_user.email)

    # Vérifier que le département a été correctement mis à jour
    assert updated_user.department == new_department
