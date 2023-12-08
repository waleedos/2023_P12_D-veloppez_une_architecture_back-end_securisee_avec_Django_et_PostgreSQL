import logging  # Importer le module de logging pour enregistrer les logs
import os  # Importer le module os pour interagir avec le système d'exploitation
import re  # Importer le module re pour les expressions régulières
import jwt  # Importer le module jwt pour les JSON Web Tokens
import django  # Importer le framework Django
from django.conf import settings  # Importer les settings de Django
from django.contrib.auth import authenticate  # Importer la fonction d'authentification de Django
from epic_auth_app.models import Utilisateur  # Importer le modèle Utilisateur de l'application epic_auth_app
from django.core.exceptions import ValidationError, PermissionDenied  # Importer les exceptions spécifiques de Django
from prettytable import PrettyTable  # Importer PrettyTable pour afficher des tableaux dans la console
from filtres import filtrer_utilisateurs_par_departement, afficher_utilisateurs  # Importer les fonctions personnalisées

logger = logging.getLogger(__name__)  # Créer un logger pour ce module spécifique

# Configurer l'environnement Django pour pouvoir utiliser ses composants
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_events.settings')
django.setup()

current_authenticated_user = None  # Initialiser la variable pour l'utilisateur authentifié


def input_with_prompt(prompt):
    return input(prompt).strip()  # Lire l'entrée de l'utilisateur et retirer les espaces superflus


def gerer_utilisateurs(current_authenticated_user):
    while True:  # Boucle infinie pour le menu de gestion des utilisateurs
        logger.info("Menu de gestion des utilisateurs affiché")  # Logger l'affichage du menu
        # Afficher le menu de gestion des utilisateurs avec des couleurs spécifiques
        print("\n\033[38;5;202mGestion des Utilisateurs\033[0m\n")
        print("1. Afficher tous les Utilisateurs")
        print("2. Créer un nouvel Utilisateur")
        print("3. Supprimer un Utilisateur")
        print("4. Réaffecter un Utilisateur")
        print("5. Mettre à jour un Utilisateur")
        print("6. Filtrer les utilisateurs par Département")
        print("7. Revenir au menu précédent\n")

        user_action = input("\033[96mChoisissez l'action : \033[0m")  # Demander à l'utilisateur de choisir une action
        logger.info(f"Action choisie par l'utilisateur : {user_action}")  # Logger l'action choisie

        # Gérer le choix de l'utilisateur et appeler les fonctions correspondantes
        if user_action == '1':
            logger.info("Option choisie : Afficher tous les Utilisateurs")
            list_users()
        elif user_action == '2':
            logger.info("Option choisie : Créer un nouvel Utilisateur")
            create_user()
        elif user_action == '3':
            logger.info("Option choisie : Supprimer un Utilisateur")
            email_to_delete = input("Entrez l'email de l'utilisateur à supprimer : ")
            delete_user(current_authenticated_user.email, email_to_delete)
        elif user_action == '4':
            logger.info("Option choisie : Réaffecter un Utilisateur")
            email_to_reassign = input("Entrez l'email de l'utilisateur à réaffecter : ")
            new_department = input("Entrez le nouveau département : ")
            reassign_user(email_to_reassign, new_department, current_authenticated_user.email)
        elif user_action == '5':
            logger.info("Option choisie : Mettre à jour un Utilisateur")
            email_to_update = input("Entrez l'email de l'utilisateur à mettre à jour : ")
            update_user(current_authenticated_user, email_to_update)
        elif user_action == '6':
            logger.info("Option choisie : Filtrer les utilisateurs par Département")
            print("Choisissez un département pour filtrer :")
            print("\n\033[33mADM - Administration / GES - Gestion / "
                  "COM - Commercial / SUP - Support / AUT - Autres\n\033[0m")
            departement_code = input("Entrez le code du département : ")
            utilisateurs = filtrer_utilisateurs_par_departement(departement_code)
            afficher_utilisateurs(utilisateurs)
        elif user_action == '7':
            logger.info("Retour au menu principal")
            break
        else:
            logger.warning("Choix invalide entré dans le menu de gestion des utilisateurs")
            print("\033\n[91mChoix invalide. Veuillez réessayer.\033\n[0m")


def validate_password_strength(password):
    # Valider la force du mot de passe en vérifiant sa longueur et la présence de différents types de caractères
    if len(password) < 8 or \
       not re.search("[a-z]", password) or \
       not re.search("[A-Z]", password) or \
       not re.search("[0-9]", password):
        # Lever une exception si le mot de passe ne respecte pas les critères
        raise ValidationError("Le mot de passe doit contenir au moins 8 caractères, une lettre majuscule, "
                              "une lettre minuscule et un chiffre.")


def validate_and_create_user(email, password, first_name, last_name, phone_number, department):
    # Valider et créer un nouvel utilisateur
    try:
        # Valider l'email et la force du mot de passe
        validate_email(email)
        validate_password_strength(password)

        # Créer un nouvel utilisateur dans la base de données
        user = Utilisateur.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            department=department
        )
        # Logger l'information de la création d'un nouveau compte utilisateur
        logger.info(f"Compte créé pour {user.email}")
        # Afficher un message de confirmation dans la console
        print(f"\n\033[92mCompte créé pour {user.email}\033[0m\n")
        return user
    except ValidationError as e:
        # Gérer les erreurs de validation et les afficher
        logger.warning(f"Erreur de validation lors de la création de l'utilisateur : {e.message}")
        print(f"\n\033[91mErreur de validation : {e.message}\033[0m")
        return None


def validate_name(name, updating=False):
    # Valider un nom (prénom ou nom de famille)
    if updating and not name:
        # Autoriser un champ vide si c'est pour une mise à jour
        return None
    if not re.fullmatch(r'^[A-Za-z\s]+$', name):
        # Lever une exception si le nom contient des caractères non alphabétiques
        raise ValueError("Le nom doit contenir uniquement des caractères alphabétiques et des espaces.")
    return name


def validate_email(email):
    # Valider le format de l'email
    if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        # Lever une exception si l'email n'est pas valide
        raise ValueError("Format d'email invalide.")


def validate_phone_number(phone_number):
    # Valider le format du numéro de téléphone
    if not re.fullmatch(r'^\+?[\d\s]{10,15}$', phone_number):
        # Lever une exception si le numéro de téléphone n'est pas valide
        raise ValueError("Format de numéro de téléphone invalide.")


def create_user(email=None, password=None, first_name=None, last_name=None,
                phone_number=None, department=None):
    # Créer un nouvel utilisateur avec des valeurs par défaut ou fournies
    logger = logging.getLogger(__name__)
    # Logger le début du processus de création
    logger.info("Début de la création d'un nouvel utilisateur")

    global current_authenticated_user

    if current_authenticated_user is None:
        # Vérifier si l'utilisateur est authentifié avant de créer un nouvel utilisateur
        logger.warning("Tentative de création d'utilisateur sans authentification")
        print("\n\033[91mVous devez être connecté pour créer un utilisateur.\033[0m\n")
        return

    if not current_authenticated_user.is_superuser and \
       current_authenticated_user.department not in ['ADM', 'GES']:
        # Vérifier si l'utilisateur a les permissions nécessaires pour créer un nouvel utilisateur
        logger.warning(
            f"Tentative de création d'utilisateur par {current_authenticated_user.email} "
            "sans accréditation suffisante"
        )
        print(
            "\n\033[91mVous n'avez pas le niveau d'accréditation ADM ou GES pour pouvoir "
            "créer un utilisateur.\033[0m\n"
        )
        return

    try:
        # Collecter les informations de l'utilisateur et les valider
        email = email or input_with_prompt("Entrez l'email du nouvel utilisateur : ")
        validate_email(email)
        password = password or input_with_prompt("Entrez le mot de passe du nouvel utilisateur : ")
        first_name = first_name or input_with_prompt("Entrez le prénom du nouvel utilisateur : ")
        validate_name(first_name)
        last_name = last_name or input_with_prompt("Entrez le nom de famille du nouvel utilisateur : ")
        validate_name(last_name)
        phone_number = phone_number or input_with_prompt(
            "Entrez le numéro de téléphone du nouvel utilisateur : "
        )
        validate_phone_number(phone_number)
        department = department or input_with_prompt(
            "Entrez le département du nouvel utilisateur (COM/SUP/GES/ADM/TST) : "
        )

        # Valider et créer l'utilisateur
        validate_and_create_user(email, password, first_name, last_name, phone_number, department)
        logger.info(f"Utilisateur {email} créé avec succès")
    except ValueError as e:
        # Gérer les exceptions liées à la validation
        logger.error(f"Erreur de validation lors de la création de l'utilisateur : {e}")
        print(f"\n\033[91mErreur de validation : {e}\033[0m")


def authenticate_superuser():
    # Fonction pour authentifier un superutilisateur
    global current_authenticated_user
    logger.info("Tentative d'authentification de superutilisateur")

    # Vérifier si l'utilisateur est déjà connecté et a les permissions nécessaires
    if current_authenticated_user and current_authenticated_user.is_superuser:
        logger.info(f"Utilisateur déjà connecté en tant que superutilisateur : {current_authenticated_user.email}")
        return True

    email = input_with_prompt("Entrez votre email : ")
    password = input_with_prompt("Entrez votre mot de passe : ")
    user = authenticate(email=email, password=password)

    if user and user.is_superuser:
        logger.info(f"Superutilisateur authentifié avec succès : {email}")
        return True
    else:
        logger.warning(f"Échec de l'authentification de superutilisateur pour l'email : {email}")
        return False


def update_user(current_user, user_to_update_email):
    # Mettre à jour les informations d'un utilisateur existant
    if not current_user:
        # Vérifier si l'utilisateur actuel est authentifié
        print("\033[91mAuthentification requise.\033[0m")
        return

    logger = logging.getLogger(__name__)
    logger.info(f"Updating user {user_to_update_email}")

    try:
        # Tenter de récupérer l'utilisateur à mettre à jour depuis la base de données
        user_to_update = Utilisateur.objects.get(email=user_to_update_email)
    except Utilisateur.DoesNotExist:
        # Gérer le cas où l'utilisateur n'existe pas
        print("\033[91mAucun utilisateur trouvé avec cet email.\033[0m")
        return

    if not current_user.is_superuser and current_user.department not in ['ADM', 'GES']:
        # Vérifier si l'utilisateur actuel a les permissions nécessaires pour effectuer la mise à jour
        print("\033[91mVous n'avez pas les permissions requises des départements ADM ou GES.\033[0m\n")
        return

    try:
        # Demander et valider les nouvelles informations de l'utilisateur
        new_email = input("Entrez le nouvel email (laissez vide pour ne pas changer) : ").strip()
        if new_email:
            validate_email(new_email)
            user_to_update.email = new_email

        new_first_name = input("Entrez le nouveau prénom (laissez vide pour ne pas changer) : ").strip()
        if new_first_name:
            user_to_update.first_name = validate_name(new_first_name, updating=True)

        new_last_name = input("Entrez le nouveau nom de famille (laissez vide pour ne pas changer) : ").strip()
        if new_last_name:
            user_to_update.last_name = validate_name(new_last_name, updating=True)

        new_phone = input("Entrez le nouveau numéro de téléphone (laissez vide pour ne pas changer) : ").strip()
        if new_phone:
            validate_phone_number(new_phone)
            user_to_update.phone = new_phone

        user_to_update.save()  # Sauvegarder les modifications dans la base de données
        print("\n\033[92mUtilisateur mis à jour.\033\n[0m\n")

    except ValueError as e:
        # Gérer les erreurs de validation
        print(f"\n\033[91mErreur de validation : {e}\033\n[0m")
    except Exception as e:
        # Gérer toute autre exception
        logger.error(f'Erreur lors de la création de l’utilisateur : {e}')
        print("\033[91mErreur lors de la mise à jour de l'utilisateur.\033[0m")


def get_current_user():
    # Récupérer l'utilisateur actuellement authentifié
    global current_authenticated_user
    if current_authenticated_user:
        logger.info(f"Utilisateur actuellement connecté : {current_authenticated_user.email}")
    else:
        logger.info("Aucun utilisateur actuellement connecté")
    return current_authenticated_user


def login(email=None, password=None, show_token=True):
    # Fonction pour connecter un utilisateur
    global current_authenticated_user  # Utiliser la variable globale

    if email is None:
        email = input("Entrez votre email : ")
    if password is None:
        password = input("Entrez votre mot de passe : ")

    logger.info(f"Tentative de connexion pour l'email : {email}")

    user = authenticate(email=email, password=password)

    if user is not None:
        current_authenticated_user = user  # Mettre à jour l'utilisateur authentifié
        logger.info(f"Utilisateur {email} authentifié avec succès")
        print("\n\033[92mUtilisateur authentifié avec succès\033[0m\n")
        token = jwt.encode({'email': user.email}, settings.JWT_SECRET_KEY, algorithm='HS256')
        if show_token:
            print(f"Token JWT généré : {token}")
        return user
    else:
        logger.warning(f"Échec de l'authentification pour l'utilisateur {email}")
        print("\033\n[91mÉchec de l'authentification pour l'utilisateur\033\n[0m")
        return None


def logout():
    # Fonction pour déconnecter l'utilisateur actuel
    global current_authenticated_user
    if current_authenticated_user:
        logger.info(f"Utilisateur {current_authenticated_user.email} déconnecté")
    else:
        logger.info("Tentative de déconnexion sans utilisateur connecté")

    current_authenticated_user = None  # Réinitialiser l'utilisateur authentifié
    print("\n\033[92mVous êtes maintenant déconnecté\033[0m\n")


def list_users():
    # Afficher la liste de tous les utilisateurs
    logger.info("Affichage de la liste des utilisateurs")

    users = Utilisateur.objects.all().order_by('department')  # Récupérer tous les utilisateurs, triés par département
    table = PrettyTable()  # Créer une table pour l'affichage
    # Définir les noms des colonnes de la table
    table.field_names = [" ID ", " Email ", " First Name ", " Last Name ", " Department ", " Is Superuser "]
    table.border = False  # Pas de bordure pour la table
    table.header = True  # Afficher l'en-tête de la table
    table.align = 'l'  # Aligner le texte à gauche

    if users.exists():  # Vérifier s'il y a des utilisateurs à afficher
        for user in users:  # Itérer sur chaque utilisateur
            # Ajouter une ligne à la table pour chaque utilisateur
            table.add_row([
                " " + str(user.id) + " ",
                " " + user.email + " ",
                " " + user.first_name + " ",
                " " + user.last_name + " ",
                " " + user.department + " ",
                " Yes " if user.is_superuser else " No ",
            ])

        # Calculer la largeur maximale pour l'affichage de la bordure
        max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
        border_line = '\033[94m╠' + '═' * (max_width - 2) + '╣\033[0m'

        # Afficher la table avec des bordures colorées
        print('\033[94m╔' + '═' * (max_width - 2) + '╗\033[0m')
        for i, line in enumerate(table.get_string().split("\n")):
            print('\033[94m║' + line.ljust(max_width - 2) + '║\033[0m')
            if i == 0:
                print(border_line)
        print('\033[94m╚' + '═' * (max_width - 2) + '╝\033[0m')
    else:
        # Si aucun utilisateur n'est disponible, logger un avertissement
        logger.warning("Aucun utilisateur n'est disponible pour l'affichage")
        print("\033[93mAucun utilisateur disponible.\033[0m")


def delete_user(requesting_user_email, user_to_delete_email):
    # Supprimer un utilisateur spécifié
    try:
        # Tenter de récupérer les informations des utilisateurs impliqués
        requesting_user = Utilisateur.objects.get(email=requesting_user_email)
        user_to_delete = Utilisateur.objects.get(email=user_to_delete_email)

        # Vérifier si l'utilisateur qui a fait la demande a les autorisations nécessaires
        if not (requesting_user.is_superuser or requesting_user.department in ['ADM', 'GES']):
            # Logger un avertissement en cas de permissions insuffisantes
            logger.warning(
                f"Tentative de suppression de l'utilisateur {user_to_delete_email} "
                f"refusée pour {requesting_user_email}"
            )
            # Lever une exception pour un manque d'accréditation
            raise PermissionDenied(
                "\n\033[91mVous n'avez pas le niveau d'accréditation (ADM ou GES), nécessaire "
                "pour supprimer cet utilisateur.\n"
            )

        user_to_delete.delete()  # Supprimer l'utilisateur de la base de données
        # Logger l'information de la suppression
        logger.info(f"Utilisateur {user_to_delete_email} supprimé par {requesting_user_email}")
        # Afficher un message de confirmation
        print(f"\n\033[92mUtilisateur {user_to_delete_email} supprimé avec succès.\033\n[0m")

    except Utilisateur.DoesNotExist:
        # Gérer le cas où l'utilisateur n'existe pas
        logger.error(
            f"Utilisateur {user_to_delete_email} ou demandeur {requesting_user_email} non trouvé"
        )
        print("\033[91mUtilisateur non trouvé.\033[0m\n")
    except PermissionDenied as e:
        # Afficher le message d'erreur en cas de PermissionDenied
        print(f"\033[91m{e}\033[0m\n")
    except Exception as e:
        # Gérer toute autre exception
        logger.exception("Erreur lors de la suppression d'un utilisateur")
        print(f"\033[91mUne erreur s'est produite : {e}\033[0m\n")


def validate_department(department):
    # Valider si le département est valide
    valid_departments = ['COM', 'SUP', 'GES', 'ADM', 'TST']  # Liste des départements valides
    if department not in valid_departments:
        # Lever une exception si le département n'est pas valide
        raise ValueError(f"Département invalide. Les départements valides sont : {', '.join(valid_departments)}.")


def reassign_user(email, new_department, current_user_email):
    # Réaffecter un utilisateur à un nouveau département
    logger.info(
        f"Tentative de réaffectation de l'utilisateur : {email} au département : {new_department}"
    )

    try:
        # Récupérer les informations de l'utilisateur actuel
        current_user = Utilisateur.objects.get(email=current_user_email)
        # Vérifier si l'utilisateur actuel a les permissions nécessaires
        if not current_user.is_superuser and current_user.department != 'ADM':
            logger.warning(
                f"Accès refusé pour la réaffectation par l'utilisateur : {current_user_email}"
            )
            print(
                "\n\033[91mAccès refusé. Seuls les superutilisateurs ou les utilisateurs du "
                "département ADM peuvent réaffecter des utilisateurs.\033[0m\n"
            )
            return

        user = Utilisateur.objects.get(email=email)  # Récupérer l'utilisateur à réaffecter
        validate_department(new_department)  # Valider le nouveau département
        user.department = new_department  # Mettre à jour le département
        user.save()  # Sauvegarder les modifications
        logger.info(
            f"Utilisateur {email} réaffecté avec succès au département {new_department}"
        )
        # Afficher un message de confirmation
        print(
            f"\033[92mUtilisateur {email} ré-affecté au département {new_department}.\033[0m\n"
        )
    except Utilisateur.DoesNotExist:
        # Gérer le cas où l'utilisateur n'existe pas
        logger.error(f"Utilisateur non trouvé pour l'email : {email}")
        print("\033[91mAucun utilisateur trouvé avec cet email.\033[0m\n")
    except ValueError as e:
        # Gérer les erreurs de validation
        logger.error(
            f"Erreur de validation lors de la réaffectation de l'utilisateur : {e}"
        )
        print(f"\n\033[91mErreur de validation : {e}\033[0m\n")
    except Exception as e:
        # Gérer toute autre exception
        logger.error(
            f"Erreur inattendue lors de la réaffectation de l'utilisateur : {e}"
        )
        print(f"\033[91mErreur lors de la ré-affectation de l'utilisateur : {e}\033[0m\n")
