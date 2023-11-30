import os
import django
from django.utils import timezone
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from prettytable import PrettyTable

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
        print("4. Supprimer un Client")
        print("5. Revenir au menu précédent\n")

        choix_client = input("\033[96mChoisissez une action: \033[0m")

        if choix_client == '1':
            list_clients()  # Appel de la fonction list_clients pour afficher tous les clients
        elif choix_client == '2':
            add_client(current_user)  # Logique pour ajouter un nouveau client
        elif choix_client == '3':
            update_client(current_user)  # Logique pour modifier un client
        elif choix_client == '4':
            delete_client(current_user)  # Logique pour supprimer un client
        elif choix_client == '5':
            break  # Sortir de la boucle pour revenir au menu principal
        else:
            print("\033[91mChoix invalide. Veuillez réessayer.\033[0m")


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


def add_client(current_user):
    if not current_user or current_user.department != 'COM':
        print("\033[91mAccès refusé. Seuls les membres de l'équipe commerciale peuvent ajouter des clients.\033[0m")
        return

    full_name = input("Enter full name: ").strip()
    email = input("Enter email: ").strip()
    phone_number = input("Enter phone number: ").strip()
    company_name = input("Enter company name: ").strip()

    # Validation des champs
    if not full_name:
        print("Le nom complet ne peut pas être vide.")
        return
    if not is_valid_email(email):
        print("Invalid email format.")
        return
    if not phone_number:
        print("Le numéro de téléphone ne peut pas être vide.")
        return
    if not company_name:
        print("Le nom de l'entreprise ne peut pas être vide.")
        return

    client = Client(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        company_name=company_name,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    client.save()
    print(f"\033[92mClient {full_name} added successfully.\033[0m")


def list_clients():
    clients = Client.objects.all()
    table = PrettyTable()
    table.field_names = [" ID ", " Nom ", " Email ", " Téléphone ", " Entreprise "]
    table.border = False
    table.header = True  # Activer l'affichage des en-têtes
    table.align = 'l'

    # Ajout des lignes de clients au tableau
    for client in clients:
        table.add_row([
            " " + str(client.id) + " ",
            " " + client.full_name + " ",
            " " + client.email + " ",
            " " + client.phone_number + " ",
            " " + client.company_name + " ",
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
    print(f"Current user department: {current_user.department if current_user else 'None'}")  # Ajouter pour le débogage
    if not current_user or current_user.department not in ['COM', 'SUP', 'GES']:
        print("\033[91mAccès refusé. Vous n'avez pas les permissions nécessaires.\033[0m")
        return

    list_clients()
    client = get_client_by_id()
    if client:
        new_full_name = input("Enter new full name (leave blank to not change): ").strip()
        new_email = input("Enter new email (leave blank to not change): ").strip()
        new_phone_number = input("Enter new phone number (leave blank to not change): ").strip()
        new_company_name = input("Enter new company name (leave blank to not change): ").strip()

        if new_full_name:
            client.full_name = new_full_name
        if new_email and is_valid_email(new_email):
            client.email = new_email
        elif new_email:
            print("Invalid email format.")
            return
        if new_phone_number:
            client.phone_number = new_phone_number
        if new_company_name:
            client.company_name = new_company_name

        client.updated_at = timezone.now()
        client.save()
        print(f"Client {client.full_name} updated successfully.")
    else:
        print("Update cancelled.")


def delete_client(current_user):
    # Vérifier les permissions de l'utilisateur
    if not current_user or current_user.department not in ['COM', 'SUP', 'GES']:
        print("\033[91mAccès refusé.\n")
        print("Seuls les membres des équipes commerciale, support ou management peuvent supprimer des clients.\033[0m")
        return

    list_clients()  # Afficher la liste des clients
    client = get_client_by_id()
    if client:
        confirm = input(f"Are you sure you want to delete {client.full_name}? (yes/no): ")
        if confirm.lower() == 'yes':
            client.delete()
            print("\033[92mClient deleted successfully.\033[0m")
        else:
            print("Deletion cancelled.")
    else:
        print("Deletion cancelled.")
