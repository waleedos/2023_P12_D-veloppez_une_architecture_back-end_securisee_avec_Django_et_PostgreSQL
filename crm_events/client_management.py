import os
import re
import django
from django.utils import timezone
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from prettytable import PrettyTable
from epic_auth_app.models import Utilisateur

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_events.settings')
django.setup()

from epic_clients_app.models import Client  # noqa: E402


def is_valid_email(email):
    try:
        EmailValidator()(email)
        return True
    except ValidationError:
        return False


def gerer_clients(current_user):
    while True:
        print("\033[38;5;202mGestion des Clients\033[0m\n")
        print("1. Afficher tous les Clients")
        print("2. Ajouter un nouveau Client")
        print("3. Modifier un Client")
        print("4. Revenir au menu précédent\n")

        choix_client = input("\033[96mChoisissez une action: \033[0m")

        if choix_client == '1':
            list_clients()  # Appel de la fonction list_clients pour afficher tous les clients
        elif choix_client == '2':
            add_client(current_user)  # Logique pour ajouter un nouveau client
        elif choix_client == '3':
            update_client(current_user)  # Logique pour modifier un client
        elif choix_client == '4':
            break  # Sortir de la boucle pour revenir au menu principal
        else:
            print("\033\n[91mChoix invalide. Veuillez réessayer.\033\n[0m")


def get_client_by_id():
    while True:
        try:
            client_id = int(input("Enter client ID: "))
            client = Client.objects.get(id=client_id)
            return client
        except ValueError:
            print("Please enter a valid number.")
        except Client.DoesNotExist:
            print("No client found with the given ID.")
            if input("Try again? (yes/no): ").lower() != 'yes':
                return None


def validate_name(name):
    if not re.fullmatch(r'^[A-Za-z\s]+$', name):
        raise ValueError("Le nom doit contenir uniquement des caractères alphabétiques et des espaces.")


def validate_email(email):
    if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise ValueError("Format d'email invalide.")


def validate_phone_number(phone_number):
    if not re.fullmatch(r'^\+?[\d\s]{10,15}$', phone_number):
        raise ValueError("\n\033[91mFormat de numéro de téléphone invalide.\033[0m")


def add_client(current_user):
    if not current_user or current_user.department != 'COM':
        print("\033[91mAccès refusé. Seuls les membres de l'équipe commerciale peuvent ajouter des clients.\033[0m")
        return

    try:
        full_name = input("Enter full name: ").strip()
        email = input("Enter email: ").strip()
        phone_number = input("Enter phone number: ").strip()
        company_name = input("Enter company name: ").strip()

        # Appliquer les validations
        validate_name(full_name)
        validate_email(email)
        validate_phone_number(phone_number)

        if not company_name:
            print("Le nom de l'entreprise ne peut pas être vide.")
            return

        # Création du client avec le commercial assigné
        client = Client(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            commercial_assigne=current_user,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        client.save()
        print(f"\033[92mClient {full_name} added successfully.\033\n[0m")

    except ValueError as e:
        print(e)


def list_clients():
    clients = Client.objects.all()
    table = PrettyTable()
    table.field_names = [" ID ", " Nom ", " Email ", " Téléphone ", " Entreprise ", " Commercial Assigné "]
    table.border = False
    table.header = True  # Activer l'affichage des en-têtes
    table.align = 'l'

    # Ajout des lignes de clients au tableau
    for client in clients:
        commercial_assigne = client.commercial_assigne.get_full_name() if client.commercial_assigne else 'Non Assigné'
        table.add_row([
            " " + str(client.id) + " ",
            " " + client.full_name + " ",
            " " + client.email + " ",
            " " + client.phone_number + " ",
            " " + client.company_name + " ",
            " " + commercial_assigne + " ",
        ])

    # Calcul de la largeur maximale pour l'affichage
    max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
    border_line = '\033[33m╠' + '═' * (max_width - 2) + '╣\033[0m'  # Couleur orange pour la bordure

    # Affichage du tableau avec les bordures personnalisées et en orange
    print('\033[33m╔' + '═' * (max_width - 2) + '╗\033[0m')
    for i, line in enumerate(table.get_string().split("\n")):
        print('\033[33m║' + line.ljust(max_width - 2) + '║\033[0m')
        if i == 0:  # Après l'en-tête
            print(border_line)
    print('\033[33m╚' + '═' * (max_width - 2) + '╝\033[0m')


def update_client(current_user):
    print(f"Current user department: {current_user.department if current_user else 'None'}")
    if not current_user or current_user.department not in ['COM', 'ADM']:
        print("\n\033[91mAccès refusé. Vous n'avez pas les permissions nécessaires.\033\n[0m")
        return

    list_clients()  # Afficher la liste des clients avec la colonne commercial assigné
    client_id = input("Enter the ID of the client to update: ").strip()

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        print("\n\033[91mClient not found.\033\n[0m")
        return

    while True:
        try:
            new_full_name = input("Enter new full name (leave blank to not change): ").strip()
            new_email = input("Enter new email (leave blank to not change): ").strip()
            new_phone_number = input("Enter new phone number (leave blank to not change): ").strip()
            new_company_name = input("Enter new company name (leave blank to not change): ").strip()
            new_commercial_assigne_id = input("Enter new commercial ID (leave blank to not change): ").strip()

            # Appliquer les validations
            if new_full_name:
                validate_name(new_full_name)
                client.full_name = new_full_name
            if new_email:
                validate_email(new_email)
                client.email = new_email
            if new_phone_number:
                validate_phone_number(new_phone_number)
                client.phone_number = new_phone_number
            if new_company_name:
                client.company_name = new_company_name

            # Mise à jour du commercial assigné si nécessaire
            if new_commercial_assigne_id:
                new_commercial = Utilisateur.objects.get(id=new_commercial_assigne_id)
                client.commercial_assigne = new_commercial

            client.updated_at = timezone.now()
            client.save()
            print(f"\n\033[92mClient {client.full_name} updated successfully.\033\n[0m")
            break  # Sortie de la boucle après succès

        except ValueError as e:
            print(e)  # Affiche l'erreur et redemande les données
        except Utilisateur.DoesNotExist:
            print("Commercial not found.")
            continue  # Demande à nouveau les données
