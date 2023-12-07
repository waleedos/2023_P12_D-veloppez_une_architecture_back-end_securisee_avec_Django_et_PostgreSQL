import logging
import os
import re
import django
from django.utils import timezone
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from prettytable import PrettyTable
from epic_auth_app.models import Utilisateur

logger = logging.getLogger(__name__)

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
    logger.info(f"Accès à la gestion des clients par l'utilisateur: {current_user.email if current_user else 'None'}")

    while True:
        print("\033[38;5;202mGestion des Clients\033[0m\n")
        print("1. Afficher tous les Clients")
        print("2. Ajouter un nouveau Client")
        print("3. Modifier un Client")
        print("4. Revenir au menu précédent\n")

        choix_client = input("\033[96mChoisissez une action: \033[0m")

        if choix_client == '1':
            logger.info("Choix de l'affichage de tous les clients")
            list_clients()
        elif choix_client == '2':
            logger.info("Choix de l'ajout d'un nouveau client")
            add_client(current_user)
        elif choix_client == '3':
            logger.info("Choix de la modification d'un client")
            update_client(current_user)
        elif choix_client == '4':
            logger.info("Sortie de la gestion des clients")
            break
        else:
            logger.warning("Choix invalide dans la gestion des clients")
            print("\033\n[91mChoix invalide. Veuillez réessayer.\033\n[0m")


def get_client_by_id():
    logger.info("Début de la recherche d'un client par ID")

    while True:
        try:
            client_id = int(input("Enter client ID: "))
            client = Client.objects.get(id=client_id)
            logger.info(f"Client trouvé avec l'ID : {client_id}")
            return client
        except ValueError:
            logger.error("Erreur de format de numéro pour l'ID du client")
            print("Please enter a valid number.")
        except Client.DoesNotExist:
            logger.warning(f"Aucun client trouvé pour l'ID : {client_id}")
            print("No client found with the given ID.")
            if input("Try again? (yes/no): ").lower() != 'yes':
                return None


def validate_name(name, updating=False):
    if updating and not name:
        return name  # Permet de laisser le champ vide pour une mise à jour
    if not re.fullmatch(r'^[A-Za-z\s]+$', name):
        raise ValueError("Le nom doit contenir uniquement des caractères alphabétiques et des espaces.")
    return name


def validate_email(email):
    if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise ValueError("Format d'email invalide.")


def validate_phone_number(phone_number):
    if not re.fullmatch(r'^\+?[\d\s]{10,15}$', phone_number):
        raise ValueError("\n\033[91mFormat de numéro de téléphone invalide.\033[0m")


def add_client(current_user):
    logger.info("Début de l'ajout d'un nouveau client")

    if not current_user or current_user.department != 'COM':
        logger.warning("Accès refusé à l'ajout de client - utilisateur non autorisé")
        print("\n\033[91mAccès refusé. Seuls les membres de l'équipe commerciale peuvent ajouter des clients.\033[0m")
        return

    try:
        full_name = input("Enter full name: ").strip()
        email = input("Enter email: ").strip()
        phone_number = input("Enter phone number: ").strip()
        company_name = input("Enter company name: ").strip()

        validate_name(full_name)
        validate_email(email)
        validate_phone_number(phone_number)

        if not company_name:
            logger.warning("Le nom de l'entreprise est vide lors de l'ajout du client")
            print("Le nom de l'entreprise ne peut pas être vide.")
            return

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
        logger.info(f"Client {full_name} ajouté avec succès")
        print(f"\033[92mClient {full_name} added successfully.\033\n[0m")

    except ValueError as e:
        logger.error(f"Erreur lors de l'ajout du client : {e}")
        print(e)


def list_clients():
    logger.info("Affichage de la liste des clients")

    clients = Client.objects.all()

    if not clients:
        logger.warning("Aucun client à afficher")
        print("\033[93mAucun client disponible.\033[0m")
        return

    table = PrettyTable()
    table.field_names = [" ID ", " Nom ", " Email ", " Téléphone ", " Entreprise ", " Commercial Assigné "]
    table.border = False
    table.header = True
    table.align = 'l'

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

    max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
    border_line = '\033[33m╠' + '═' * (max_width - 2) + '╣\033[0m'

    print('\033[33m╔' + '═' * (max_width - 2) + '╗\033[0m')
    for i, line in enumerate(table.get_string().split("\n")):
        print('\033[33m║' + line.ljust(max_width - 2) + '║\033[0m')
        if i == 0:
            print(border_line)
    print('\033[33m╚' + '═' * (max_width - 2) + '╝\033[0m')

    logger.info("Liste des clients affichée avec succès")


def update_client(current_user):
    logger.info(
        f"Tentative de mise à jour d'un client par l'utilisateur: "
        f"{current_user.email if current_user else 'None'}"
    )

    if not current_user or current_user.department not in ['COM', 'ADM']:
        logger.warning("Accès refusé pour la mise à jour du client - permissions insuffisantes")
        print("\n\033[91mAccès refusé. Vous n'avez pas les permissions nécessaires.\033\n[0m")
        return

    list_clients()

    try:
        client_id = input("Enter the ID of the client to update: ").strip()
        client = Client.objects.get(id=client_id)

        new_full_name = input("Enter new full name (leave blank to not change): ").strip()
        new_email = input("Enter new email (leave blank to not change): ").strip()
        new_phone_number = input("Enter new phone number (leave blank to not change): ").strip()
        new_company_name = input("Enter new company name (leave blank to not change): ").strip()
        new_commercial_assigne_id = input("Enter new commercial ID (leave blank to not change): ").strip()

        if new_full_name:
            client.full_name = validate_name(new_full_name, updating=True)
        if new_email:
            validate_email(new_email)
            client.email = new_email
        if new_phone_number:
            validate_phone_number(new_phone_number)
            client.phone_number = new_phone_number
        if new_company_name:
            client.company_name = new_company_name
        if new_commercial_assigne_id:
            new_commercial = Utilisateur.objects.get(id=new_commercial_assigne_id)
            client.commercial_assigne = new_commercial

        client.updated_at = timezone.now()
        client.save()
        logger.info(f"Client mis à jour avec succès : {client.full_name}")
        print(f"\n\033[92mClient {client.full_name} mis à jour avec succès.\033\n[0m")

    except ValueError as e:
        logger.error(f"Erreur lors de la mise à jour du client : {e}")
        print(e)
    except Utilisateur.DoesNotExist:
        logger.error("Commercial assigné introuvable.")
        print("Commercial not found.")
    except Client.DoesNotExist:
        logger.error(f"Client introuvable pour l'ID : {client_id}")
        print("\n\033[91mClient not found.\033\n[0m")
