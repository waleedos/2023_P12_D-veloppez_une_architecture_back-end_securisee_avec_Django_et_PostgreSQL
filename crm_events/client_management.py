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
# Création d'un logger pour enregistrer les événements de ce script.

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_events.settings')
django.setup()
# Configuration de l'environnement Django pour le projet 'crm_events'.

from epic_clients_app.models import Client  # noqa: E402
# Importation du modèle Client après l'initialisation de Django.


def is_valid_email(email):
    # Définition d'une fonction pour valider une adresse email.

    try:
        EmailValidator()(email)
        return True
        # Utilisation du validateur d'email de Django et retourne True si l'email est valide.

    except ValidationError:
        return False
        # Retourne False si une exception de validation est levée.


def gerer_clients(current_user):
    # Définition d'une fonction pour gérer les interactions avec les clients.

    logger.info(f"Accès à la gestion des clients par l'utilisateur: {current_user.email if current_user else 'None'}")
    # Enregistrement de l'accès à la fonction dans le logger.

    while True:
        # Boucle infinie pour le menu de gestion des clients.

        print("\033[38;5;202mGestion des Clients\033[0m\n")
        print("1. Afficher tous les Clients")
        print("2. Ajouter un nouveau Client")
        print("3. Modifier un Client")
        print("4. Revenir au menu précédent\n")
        # Affichage des options du menu.

        choix_client = input("\033[96mChoisissez une action: \033[0m")
        # Demande de choix à l'utilisateur.

        if choix_client == '1':
            logger.info("Choix de l'affichage de tous les clients")
            list_clients()
            # Affichage de tous les clients.

        elif choix_client == '2':
            logger.info("Choix de l'ajout d'un nouveau client")
            add_client(current_user)
            # Ajout d'un nouveau client.

        elif choix_client == '3':
            logger.info("Choix de la modification d'un client")
            update_client(current_user)
            # Modification d'un client.

        elif choix_client == '4':
            logger.info("Sortie de la gestion des clients")
            break
            # Sortie de la boucle de gestion des clients.

        else:
            logger.warning("Choix invalide dans la gestion des clients")
            print("\033\n[91mChoix invalide. Veuillez réessayer.\033\n[0m")
            # Gestion des choix invalides.


def get_client_by_id():
    # Définition d'une fonction pour obtenir un client par son ID.

    logger.info("Début de la recherche d'un client par ID")
    # Enregistrement du début de la recherche dans le logger.

    while True:
        # Boucle infinie pour la saisie de l'ID du client.

        try:
            client_id = int(input("Enter client ID: "))
            client = Client.objects.get(id=client_id)
            logger.info(f"Client trouvé avec l'ID : {client_id}")
            return client
            # Récupération et retour du client par son ID.

        except ValueError:
            logger.error("Erreur de format de numéro pour l'ID du client")
            print("Please enter a valid number.")
            # Gestion d'une erreur de format de l'ID.

        except Client.DoesNotExist:
            logger.warning(f"Aucun client trouvé pour l'ID : {client_id}")
            print("No client found with the given ID.")
            if input("Try again? (yes/no): ").lower() != 'yes':
                return None
            # Gestion de l'absence d'un client avec l'ID spécifié.


def validate_name(name, updating=False):
    # Définition d'une fonction pour valider le nom.

    if updating and not name:
        return name  # Permet de laisser le champ vide pour une mise à jour
        # Si la fonction est utilisée pour une mise à jour, permettre un nom vide.

    if not re.fullmatch(r'^[A-Za-z\s]+$', name):
        raise ValueError("Le nom doit contenir uniquement des caractères alphabétiques et des espaces.")
        # Vérifie si le nom contient uniquement des caractères alphabétiques et des espaces. Sinon, lève une exception.

    return name
    # Retourne le nom si valide.


def validate_email(email):
    # Définition d'une fonction pour valider un email.

    if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise ValueError("Format d'email invalide.")
        # Vérifie le format de l'email. Si invalide, lève une exception.


def validate_phone_number(phone_number):
    # Définition d'une fonction pour valider un numéro de téléphone.

    if not re.fullmatch(r'^\+?[\d\s]{10,15}$', phone_number):
        raise ValueError("\n\033[91mFormat de numéro de téléphone invalide.\033[0m")
        # Vérifie le format du numéro de téléphone. Si invalide, lève une exception avec un message coloré.


def add_client(current_user):
    # Définition d'une fonction pour ajouter un nouveau client.

    logger.info("Début de l'ajout d'un nouveau client")
    # Enregistrement du début de l'ajout d'un client dans le logger.

    if not current_user or current_user.department != 'COM':
        logger.warning("Accès refusé à l'ajout de client - utilisateur non autorisé")
        print("\n\033[91mAccès refusé. Seuls les membres de l'équipe commerciale peuvent ajouter des clients.\n\033[0m")
        return
        # Vérification des droits de l'utilisateur actuel. Si non autorisé, affiche un message et retourne.

    try:
        full_name = input("Enter full name: ").strip()
        email = input("Enter email: ").strip()
        phone_number = input("Enter phone number: ").strip()
        company_name = input("Enter company name: ").strip()
        # Collecte des informations du nouveau client.

        validate_name(full_name)
        validate_email(email)
        validate_phone_number(phone_number)
        # Validation des informations collectées.

        if not company_name:
            logger.warning("Le nom de l'entreprise est vide lors de l'ajout du client")
            print("Le nom de l'entreprise ne peut pas être vide.")
            return
            # Vérification que le nom de l'entreprise n'est pas vide.

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
        # Création et enregistrement du nouveau client dans la base de données.

    except ValueError as e:
        logger.error(f"Erreur lors de l'ajout du client : {e}")
        print(e)
        # Gestion des erreurs de validation avec enregistrement dans le logger et affichage de l'erreur.


def list_clients():
    # Définition d'une fonction pour lister les clients.

    logger.info("Affichage de la liste des clients")
    # Enregistrement de l'action dans le logger.

    clients = Client.objects.all()
    # Récupération de tous les clients.

    if not clients:
        logger.warning("Aucun client à afficher")
        print("\033[93mAucun client disponible.\033[0m")
        return
        # Si aucun client n'est trouvé, affiche un message et retourne.

    table = PrettyTable()
    table.field_names = [" ID ", " Nom ", " Email ", " Téléphone ", " Entreprise ", " Commercial Assigné "]
    table.border = False
    table.header = True
    table.align = 'l'
    # Configuration de la table pour l'affichage des clients.

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
        # Ajout des clients dans la table.

    max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
    border_line = '\033[33m╠' + '═' * (max_width - 2) + '╣\033[0m'

    print('\033[33m╔' + '═' * (max_width - 2) + '╗\033[0m')
    for i, line in enumerate(table.get_string().split("\n")):
        print('\033[33m║' + line.ljust(max_width - 2) + '║\033[0m')
        if i == 0:
            print(border_line)
    print('\033[33m╚' + '═' * (max_width - 2) + '╝\033[0m')
    # Affichage de la table avec un design personnalisé.

    logger.info("Liste des clients affichée avec succès")
    # Enregistrement de la réussite de l'affichage dans le logger.


def update_client(current_user):
    # Définition d'une fonction pour mettre à jour les informations d'un client.

    logger.info(
        f"Tentative de mise à jour d'un client par l'utilisateur: "
        f"{current_user.email if current_user else 'None'}"
    )
    # Enregistrement de la tentative de mise à jour dans le logger.

    if not current_user or current_user.department not in ['COM', 'ADM']:
        logger.warning("Accès refusé pour la mise à jour du client - permissions insuffisantes")
        print("\n\033[91mAccès refusé. Vous n'avez pas les permissions nécessaires.\033\n[0m")
        return
        # Vérification des permissions de l'utilisateur actuel.

    list_clients()
    # Affichage de la liste des clients pour aider à choisir le client à mettre à jour.

    try:
        client_id = input("Enter the ID of the client to update: ").strip()
        client = Client.objects.get(id=client_id)
        # Récupération du client à partir de l'ID saisi.

        new_full_name = input("Enter new full name (leave blank to not change): ").strip()
        new_email = input("Enter new email (leave blank to not change): ").strip()
        new_phone_number = input("Enter new phone number (leave blank to not change): ").strip()
        new_company_name = input("Enter new company name (leave blank to not change): ").strip()
        new_commercial_assigne_id = input("Enter new commercial ID (leave blank to not change): ").strip()
        # Saisie des nouvelles informations pour le client.

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
        # Mise à jour des informations du client après validation.

        client.updated_at = timezone.now()
        client.save()
        logger.info(f"Client mis à jour avec succès : {client.full_name}")
        print(f"\n\033[92mClient {client.full_name} mis à jour avec succès.\033\n[0m")
        # Enregistrement des modifications et notification de la mise à jour réussie.

    except ValueError as e:
        logger.error(f"Erreur lors de la mise à jour du client : {e}")
        print(e)
        # Gestion des erreurs de validation avec enregistrement dans le logger et affichage de l'erreur.

    except Utilisateur.DoesNotExist:
        logger.error("Commercial assigné introuvable.")
        print("Commercial not found.")
        # Gestion de l'erreur si le commercial assigné n'existe pas.

    except Client.DoesNotExist:
        logger.error(f"Client introuvable pour l'ID : {client_id}")
        print("\n\033[91mClient not found.\033\n[0m")
        # Gestion de l'erreur si le client n'existe pas.
