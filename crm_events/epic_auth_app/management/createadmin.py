from django.core.management.base import BaseCommand
from epic_auth_app.models import Utilisateur


class Command(BaseCommand):
    help = 'Crée un superutilisateur Administration'

    def handle(self, *args, **kwargs):
        email = 'admin@example.com'  # Nous pouvons rendre ces valeurs dynamiques
        password = 'password'
        Utilisateur.objects.create_superuser(email=email, password=password, department='ADM')
        self.stdout.write(self.style.SUCCESS(f'Superutilisateur créé : {email}'))
