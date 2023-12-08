# Importation des modules nécessaires au fonctionnement du script
import logging
import re
from epic_contracts_app.models import Contrat
from epic_clients_app.models import Client
from epic_auth_app.models import Utilisateur
from client_management import list_clients
from django.core.exceptions import ValidationError
from filtres import filtrer_contrats_non_signes, filtrer_contrats_non_entierement_payes, afficher_contrats
from django.utils import timezone
from prettytable import PrettyTable

# Configuration du logger pour enregistrer les messages de log
logger = logging.getLogger(__name__)


# Définition d'une fonction pour valider le nom d'un contrat
def validate_contract_name(name):
    # Utilisation d'une expression régulière pour s'assurer que le nom contient uniquement des lettres et des espaces
    if not re.fullmatch(r'^[A-Za-z\s]+$', name):
        raise ValueError("Le nom du contrat doit contenir uniquement des caractères alphabétiques et des espaces.")


# Définition d'une fonction pour valider un montant
def validate_amount(amount):
    # Utilisation d'une expression régulière pour valider un montant avec jusqu'à deux décimales
    if not re.fullmatch(r'^\d+(\.\d{1,2})?$', amount):
        raise ValueError("Le montant doit être un nombre valide avec au maximum deux décimales.")


# Définition d'une fonction pour valider une date
def validate_date(date_str):
    try:
        # Conversion de la chaîne de caractères en date et heure tout en prenant en compte le fuseau horaire
        return timezone.make_aware(timezone.datetime.strptime(date_str, "%Y-%m-%d %H:%M"))
    except ValueError:
        raise ValueError("Format de date invalide. Utilisez le format YYYY-MM-DD HH:MM.")


# Définition d'une fonction pour créer un contrat
def create_contrat(current_user):
    # Enregistrement d'un message de log pour indiquer une tentative de création de contrat
    logger.info(f"Tentative de création d'un contrat par {current_user.email}")

    # Vérification du département de l'utilisateur pour autoriser la création du contrat
    if current_user.department not in ['GES', 'ADM']:
        # Enregistrement d'un message de log en cas d'accès non autorisé
        logger.warning(f"Accès refusé pour la création de contrat par {current_user.email}")
        print("\033[91mSeuls les membres des équipes de gestion ou d'administration peuvent créer des contrats.\033[0m\n")
        return

    # Affichage de la liste des clients
    print("\033[93mVoici la liste de tous nos clients.\033[0m")
    list_clients()

    try:
        # Demande et validation des différentes informations nécessaires à la création d'un contrat
        nom_contrat = input("Entrez le nom du contrat : ")
        validate_contract_name(nom_contrat)

        client_id = input("Entrez l'ID du client pour le contrat : ")
        client = Client.objects.get(id=client_id)

        montant_total = input("Entrez le montant total du contrat : ")
        validate_amount(montant_total)

        montant_restant = input("Entrez le montant restant : ")
        validate_amount(montant_restant)

        date_creation_str = input("Entrez la date de création du contrat (format YYYY-MM-DD HH:MM) : ")
        aware_date_creation = validate_date(date_creation_str)

        statut_abrev = input("Entrez le statut du contrat (ACT pour Actif, TER pour Terminé, ATT pour En Attente) : ")
        statut_contrat = {'ACT': 'ACTIF', 'TER': 'TERMINE', 'ATT': 'EN_ATTENTE'}.get(statut_abrev.upper(), 'EN_ATTENTE')

        # Création et enregistrement du nouveau contrat
        new_contrat = Contrat(
            nom=nom_contrat, client=client, sales_contact=current_user,
            montant_total=montant_total, montant_restant=montant_restant,
            date_creation=aware_date_creation, statut=statut_contrat
        )
        new_contrat.save()

        # Enregistrement d'un message de log pour indiquer la création réussie du contrat
        logger.info(f"Contrat '{nom_contrat}' créé avec succès pour le client {client.full_name}")
        print(f"\033[92mContrat '{nom_contrat}' créé avec succès pour le client {client.full_name}.\033\n[0m")
    except Client.DoesNotExist:
        # Enregistrement d'un message de log et affichage d'une erreur si le client n'est pas trouvé
        logger.error("Client introuvable lors de la création d'un contrat")
        print("\033[91mClient introuvable.\033[0m")
    except ValidationError as e:
        # Enregistrement et affichage d'une erreur de validation
        logger.error(f"Erreur de validation lors de la création d'un contrat: {e}")
        print(f"\n\033[91mErreur de validation : {e}\033\n[0m")
    except ValueError as e:
        # Enregistrement et affichage d'une erreur générique
        logger.error(f"Erreur lors de la création d'un contrat: {e}")
        print(f"\033[91mErreur : {e}\033\n[0m")


# Définition d'une fonction pour lister les contrats
def list_contrats(current_user):
    # Enregistrement d'un message de log pour une tentative d'affichage de la liste des contrats
    logger.info(f"Tentative d'affichage de la liste des contrats par {current_user.email}")

    # Vérification du département de l'utilisateur pour autoriser l'affichage des contrats
    if current_user.department not in ['GES', 'ADM', 'SUP', 'COM']:
        # Enregistrement d'un message de log en cas d'accès refusé
        logger.warning(f"Accès refusé pour l'affichage des contrats par {current_user.email}")
        print("\033[91mAccès refusé.\033[0m")
        return

    try:
        # Récupération de tous les contrats depuis la base de données
        contrats = Contrat.objects.all()
        # Vérification de l'existence de contrats avant de les afficher
        if contrats.exists():
            # Initialisation d'une table pour un affichage formaté des contrats
            table = PrettyTable()
            table.field_names = [
                " ID ", " Nom ", " Client ", " Montant Total ", " Montant Restant ",
                " Date de Création ", " Statut ", " Client géré par (COM) "
            ]
            table.border = False
            table.header = True
            table.align = 'l'

            # Ajout de chaque contrat à la table
            for contrat in contrats:
                # Attribution du commercial assigné ou 'N/A' si aucun n'est assigné
                commercial_assigne = (
                    contrat.client.commercial_assigne.get_full_name()
                    if contrat.client.commercial_assigne else 'N/A'
                )
                table.add_row([
                    " " + str(contrat.id) + " ",
                    " " + contrat.nom + " ",
                    " " + contrat.client.full_name + " ",
                    " " + str(contrat.montant_total) + " ",
                    " " + str(contrat.montant_restant) + " ",
                    " " + contrat.date_creation.strftime('%Y-%m-%d %H:%M') + " ",
                    " " + contrat.statut + " ",
                    " " + commercial_assigne + " "
                ])

            # Définition du bord de la table pour l'affichage
            max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
            border_line = '\033[38;5;202m╠' + '═' * (max_width - 2) + '╣\033[0m'

            # Affichage de la table avec les bordures
            print('\033[38;5;202m╔' + '═' * (max_width - 2) + '╗\033[0m')
            for i, line in enumerate(table.get_string().split("\n")):
                print('\033[38;5;202m║' + line.ljust(max_width - 2) + '║\033[0m')
                if i == 0:
                    print(border_line)
            print('\033[38;5;202m╚' + '═' * (max_width - 2) + '╝\033[0m')

            # Enregistrement d'un message de log pour l'affichage réussi des contrats
            logger.info("Liste des contrats affichée avec succès")
        else:
            # Enregistrement d'un message de log si aucun contrat n'est disponible
            logger.warning("Aucun contrat disponible à afficher")
            print("\033[93mAucun contrat disponible.\033[0m")
    except Exception as e:
        # Enregistrement et affichage d'une erreur en cas de problème lors de la récupération des contrats
        logger.error(f"Erreur lors de la récupération des contrats: {e}")
        print(f"\033[91mErreur lors de la récupération des contrats: {e}\033[0m")


# Définition d'une fonction pour mettre à jour un contrat
def update_contrat(current_user, contract_id):
    # Enregistrement d'un message de log pour une tentative de mise à jour d'un contrat
    logger.info(f"Tentative de mise à jour du contrat {contract_id} par {current_user.email}")

    # Vérification des conditions pour autoriser la modification du contrat
    if not current_user or current_user.department not in ['GES', 'COM', 'ADM']:
        # Enregistrement d'un message de log en cas d'accès refusé
        logger.warning("Accès refusé pour la modification du contrat")
        print("\033[91mSeuls les membres des équipes de gestion et administration peuvent modifier un contrat.\033[0m")
        return

    try:
        # Récupération du contrat à modifier depuis la base de données
        contrat = Contrat.objects.get(id=contract_id)
    except Contrat.DoesNotExist:
        # Enregistrement et affichage d'une erreur si le contrat n'est pas trouvé
        logger.error("Contrat non trouvé lors de la tentative de mise à jour")
        print("\033[91mContrat non trouvé.\033[0m")
        return

    # Affichage des informations actuelles du contrat à modifier
    print(f"Modification du contrat {contrat.id} pour le client {contrat.client.full_name}")

    try:
        # Demande et validation des nouvelles informations du contrat
        new_nom = input("Entrez le nouveau nom du contrat (laissez vide pour ne pas changer) : ")
        if new_nom:
            validate_contract_name(new_nom)
            contrat.nom = new_nom

        new_montant_total = input("Entrez le nouveau montant total (laissez vide pour ne pas changer) : ")
        if new_montant_total:
            validate_amount(new_montant_total)
            contrat.montant_total = new_montant_total

        new_montant_restant = input("Entrez le nouveau montant restant (laissez vide pour ne pas changer) : ")
        if new_montant_restant:
            validate_amount(new_montant_restant)
            contrat.montant_restant = new_montant_restant

        new_statut = input("Entrez le nouveau statut (ACT/Ter/Att, laissez vide pour ne pas changer) : ")
        if new_statut:
            statut_dict = {'ACT': 'ACTIF', 'TER': 'TERMINE', 'ATT': 'EN_ATTENTE'}
            contrat.statut = statut_dict.get(new_statut.upper(), contrat.statut)

        # Enregistrement des modifications dans la base de données
        contrat.save()
        # Enregistrement d'un message de log pour la mise à jour réussie du contrat
        logger.info(f"Contrat {contrat.id} mis à jour avec succès")
        print(f"\n\033[92mContrat {contrat.id} mis à jour avec succès.\033[0m")
    except ValueError as e:
        # Enregistrement et affichage d'une erreur en cas de problème lors de la mise à jour
        logger.error(f"Erreur lors de la mise à jour du contrat: {e}")
        print(f"\033[91mErreur : {e}\033[0m")


def reassign_contrat(user, contrat_id):
    # Créer ou récupérer un logger pour enregistrer les activités.
    logger = logging.getLogger(__name__)

    # Vérifier si le département de l'utilisateur est autorisé à réaffecter des contrats.
    if user.department not in ['GES', 'ADM']:
        # Enregistrer un avertissement dans le log si l'utilisateur n'est pas autorisé.
        logger.warning(f"Utilisateur non autorisé {user.email} a tenté de réaffecter "
                       f"le contrat {contrat_id}")
        # Afficher un message d'erreur formaté en rouge pour indiquer l'interdiction.
        warning_msg = ("\033[91mSeules les personnes appartenant aux équipes de "
                       "gestion et administration peuvent réaffecter un contrat.\033[0m")
        print(warning_msg)
        return

    try:
        # Essayer de récupérer le contrat spécifié par son ID.
        contrat = Contrat.objects.get(id=contrat_id)
        # Demander à l'utilisateur d'entrer l'email du nouveau contact commercial.
        new_sales_contact_email = input("Entrez le nouvel email du contact commercial: ")
        # Récupérer l'utilisateur correspondant à l'email saisi.
        new_sales_contact = Utilisateur.objects.get(email=new_sales_contact_email)
        # Réaffecter le contrat au nouveau contact commercial.
        contrat.sales_contact = new_sales_contact
        # Enregistrer les modifications du contrat.
        contrat.save()
        # Enregistrer une information dans le log indiquant la réussite de la réaffectation.
        logger.info(f"Contrat {contrat_id} réaffecté à {new_sales_contact.email} par {user.email}")
        # Afficher un message de confirmation de la réaffectation.
        print(f"Contrat {contrat_id} réaffecté à {new_sales_contact.email}.")
    except Contrat.DoesNotExist:
        # Gérer l'exception si le contrat spécifié n'existe pas.
        logger.error(f"Tentative de réaffectation d'un contrat inexistant: {contrat_id}")
        # Afficher un message d'erreur formaté en rouge indiquant que le contrat n'a pas été trouvé.
        print("\033[91mContrat non trouvé.\033[0m")
    except Utilisateur.DoesNotExist:
        # Gérer l'exception si l'utilisateur spécifié n'existe pas.
        logger.error(f"Tentative de réaffectation à un utilisateur commercial inexistant: {new_sales_contact_email}")
        # Afficher un message d'erreur formaté en rouge indiquant que l'utilisateur n'a pas été trouvé.
        print("\033[91mUtilisateur non trouvé.\033[0m")


def delete_contrat(user, contrat_id):
    # Créer ou récupérer un logger pour enregistrer les activités.
    logger = logging.getLogger(__name__)

    # Vérifier si le département de l'utilisateur est autorisé à supprimer des contrats.
    if user.department not in ['GES', 'ADM']:
        # Enregistrer un avertissement dans le log si l'utilisateur n'est pas autorisé.
        logger.warning(
            f"Utilisateur non autorisé {user.email} a tenté de supprimer le contrat {contrat_id}"
        )
        # Afficher un message d'erreur formaté en rouge pour indiquer l'interdiction.
        print(
            "\033[91mSeules les personnes des équipes de gestion et administration "
            "peuvent supprimer un contrat.\033[0m"
        )
        return

    try:
        # Essayer de récupérer le contrat spécifié par son ID pour le supprimer.
        contrat = Contrat.objects.get(id=contrat_id)
        # Supprimer le contrat de la base de données.
        contrat.delete()
        # Enregistrer une information dans le log indiquant la réussite de la suppression.
        logger.info(f"Contrat {contrat_id} supprimé avec succès par {user.email}")
        # Afficher un message de confirmation de la suppression, formaté en vert.
        print(f"\n\033[92mContrat {contrat_id} supprimé avec succès.\033\n[0m")
    except Contrat.DoesNotExist:
        # Gérer l'exception si le contrat spécifié n'existe pas.
        logger.error(f"Tentative de suppression d'un contrat inexistant: {contrat_id}")
        # Afficher un message d'erreur formaté en rouge indiquant que le contrat n'a pas été trouvé.
        print("\033[91mContrat non trouvé.\033[0m")


def gerer_contrats(current_user):
    # Créer ou récupérer un logger pour enregistrer les activités de gestion des contrats.
    logger = logging.getLogger(__name__)
    # Enregistrer une information dans le log à l'entrée dans la gestion des contrats.
    logger.info(f"Entrée dans la gestion des contrats par {current_user.email}")

    while True:
        # Afficher le menu de gestion des contrats avec diverses options.
        print("\n\033[38;5;202mGestion des Contrats\033[0m\n")
        print("1. Liste de tous les contrats")
        print("2. Créer un nouveau contrat")
        print("3. Modifier un contrat")
        print("4. Supprimer un contrat")
        print("5. Réaffecter un contrat")
        print("6. Afficher les contrats non signés")
        print("7. Afficher les contrats non entièrement payés")
        print("8. Revenir au menu principal\n")

        # Demander à l'utilisateur de choisir une option.
        choix = input("\033[96mChoisissez une action:\033[0m")
        # Exécuter l'action en fonction du choix de l'utilisateur.
        if choix == '1':
            list_contrats(current_user)
        elif choix == '2':
            create_contrat(current_user)
        elif choix == '3':
            contrat_id = input("Entrez l'ID du contrat à modifier : ")
            update_contrat(current_user, contrat_id)
        elif choix == '4':
            contrat_id = input("Entrez l'ID du contrat à supprimer : ")
            delete_contrat(current_user, contrat_id)
        elif choix == '5':
            contrat_id = input("Entrez l'ID du contrat à réaffecter : ")
            reassign_contrat(current_user, contrat_id)
        elif choix == '6':
            contrats = filtrer_contrats_non_signes()
            afficher_contrats(contrats)
        elif choix == '7':
            contrats = filtrer_contrats_non_entierement_payes()
            afficher_contrats(contrats)
        elif choix == '8':
            # Enregistrer une information dans le log à la sortie de la gestion des contrats.
            logger.info("Sortie de la gestion des contrats")
            break
        else:
            # Enregistrer un avertissement dans le log si le choix est invalide.
            logger.warning("Choix invalide dans la gestion des contrats")
            # Afficher un message d'erreur formaté en rouge pour indiquer un choix invalide.
            print("\033\n[91mChoix invalide. Veuillez réessayer.\033\n[0m")
