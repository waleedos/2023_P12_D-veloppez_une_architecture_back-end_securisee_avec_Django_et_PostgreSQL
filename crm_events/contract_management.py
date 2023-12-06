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

logger = logging.getLogger(__name__)


def validate_contract_name(name):
    if not re.fullmatch(r'^[A-Za-z\s]+$', name):
        raise ValueError("Le nom du contrat doit contenir uniquement des caractères alphabétiques et des espaces.")


def validate_amount(amount):
    if not re.fullmatch(r'^\d+(\.\d{1,2})?$', amount):
        raise ValueError("Le montant doit être un nombre valide avec au maximum deux décimales.")


def validate_date(date_str):
    try:
        return timezone.make_aware(timezone.datetime.strptime(date_str, "%Y-%m-%d %H:%M"))
    except ValueError:
        raise ValueError("Format de date invalide. Utilisez le format YYYY-MM-DD HH:MM.")


def create_contrat(current_user):
    logger.info(f"Tentative de création d'un contrat par {current_user.email}")

    if current_user.department not in ['GES', 'ADM']:
        logger.warning(f"Accès refusé pour la création de contrat par {current_user.email}")
        print("\033[91mSeuls les membres des équipes de gestion ou d'administration peuvent créer des contrats.\033[0m\n")
        return

    print("\033[93mVoici la liste de tous nos clients.\033[0m")
    list_clients()

    try:
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

        new_contrat = Contrat(
            nom=nom_contrat, client=client, sales_contact=current_user,
            montant_total=montant_total, montant_restant=montant_restant,
            date_creation=aware_date_creation, statut=statut_contrat
        )
        new_contrat.save()

        logger.info(f"Contrat '{nom_contrat}' créé avec succès pour le client {client.full_name}")
        print(f"\033[92mContrat '{nom_contrat}' créé avec succès pour le client {client.full_name}.\033\n[0m")
    except Client.DoesNotExist:
        logger.error("Client introuvable lors de la création d'un contrat")
        print("\033[91mClient introuvable.\033[0m")
    except ValidationError as e:
        logger.error(f"Erreur de validation lors de la création d'un contrat: {e}")
        print(f"\n\033[91mErreur de validation : {e}\033\n[0m")
    except ValueError as e:
        logger.error(f"Erreur lors de la création d'un contrat: {e}")
        print(f"\033[91mErreur : {e}\033\n[0m")


def list_contrats(current_user):
    logger.info(f"Tentative d'affichage de la liste des contrats par {current_user.email}")

    if current_user.department not in ['GES', 'ADM', 'SUP', 'COM']:
        logger.warning(f"Accès refusé pour l'affichage des contrats par {current_user.email}")
        print("\033[91mAccès refusé.\033[0m")
        return

    try:
        contrats = Contrat.objects.all()
        if contrats.exists():
            table = PrettyTable()
            table.field_names = [
                " ID ", " Nom ", " Client ", " Montant Total ", " Montant Restant ",
                " Date de Création ", " Statut ", " Client géré par (COM) "
            ]
            table.border = False
            table.header = True
            table.align = 'l'

            for contrat in contrats:
                commercial_assigne = contrat.client.commercial_assigne.get_full_name() if contrat.client.commercial_assigne else 'N/A'
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

            max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
            border_line = '\033[38;5;202m╠' + '═' * (max_width - 2) + '╣\033[0m'

            print('\033[38;5;202m╔' + '═' * (max_width - 2) + '╗\033[0m')
            for i, line in enumerate(table.get_string().split("\n")):
                print('\033[38;5;202m║' + line.ljust(max_width - 2) + '║\033[0m')
                if i == 0:
                    print(border_line)
            print('\033[38;5;202m╚' + '═' * (max_width - 2) + '╝\033[0m')

            logger.info("Liste des contrats affichée avec succès")
        else:
            logger.warning("Aucun contrat disponible à afficher")
            print("\033[93mAucun contrat disponible.\033[0m")
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des contrats: {e}")
        print(f"\033[91mErreur lors de la récupération des contrats: {e}\033[0m")


def update_contrat(current_user, contract_id):
    logger.info(f"Tentative de mise à jour du contrat {contract_id} par {current_user.email}")

    if not current_user or current_user.department not in ['GES', 'COM', 'ADM']:
        logger.warning("Accès refusé pour la modification du contrat")
        print("\033[91mSeuls les membres des équipes de gestion et administration peuvent modifier un contrat.\033[0m")
        return

    try:
        contrat = Contrat.objects.get(id=contract_id)
    except Contrat.DoesNotExist:
        logger.error("Contrat non trouvé lors de la tentative de mise à jour")
        print("\033[91mContrat non trouvé.\033[0m")
        return

    print(f"Modification du contrat {contrat.id} pour le client {contrat.client.full_name}")

    try:
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

        contrat.save()
        logger.info(f"Contrat {contrat.id} mis à jour avec succès")
        print(f"\n\033[92mContrat {contrat.id} mis à jour avec succès.\033[0m")
    except ValueError as e:
        logger.error(f"Erreur lors de la mise à jour du contrat: {e}")
        print(f"\033[91mErreur : {e}\033[0m")


def reassign_contrat(user, contrat_id):
    logger = logging.getLogger(__name__)

    if user.department not in ['GES', 'ADM']:
        logger.warning(f"Utilisateur non autorisé {user.email} a tenté de réaffecter le contrat {contrat_id}")
        print("\033[91mSeules les personnes appartenant aux équipes de gestion et administration peuvent réaffecter un contrat.\033[0m")
        return

    try:
        contrat = Contrat.objects.get(id=contrat_id)
        new_sales_contact_email = input("Entrez le nouvel email du contact commercial: ")
        new_sales_contact = Utilisateur.objects.get(email=new_sales_contact_email)
        contrat.sales_contact = new_sales_contact
        contrat.save()
        logger.info(f"Contrat {contrat_id} réaffecté à {new_sales_contact.email} par {user.email}")
        print(f"Contrat {contrat_id} réaffecté à {new_sales_contact.email}.")
    except Contrat.DoesNotExist:
        logger.error(f"Tentative de réaffectation d'un contrat inexistant: {contrat_id}")
        print("\033[91mContrat non trouvé.\033[0m")
    except Utilisateur.DoesNotExist:
        logger.error(f"Tentative de réaffectation à un utilisateur commercial inexistant: {new_sales_contact_email}")
        print("\033[91mUtilisateur non trouvé.\033[0m")


def delete_contrat(user, contrat_id):
    logger = logging.getLogger(__name__)

    if user.department not in ['GES', 'ADM']:
        logger.warning(f"Utilisateur non autorisé {user.email} a tenté de supprimer le contrat {contrat_id}")
        print("\033[91mSeules les personnes des équipes de gestion et administration peuvent supprimer un contrat.\033[0m")
        return

    try:
        contrat = Contrat.objects.get(id=contrat_id)
        contrat.delete()
        logger.info(f"Contrat {contrat_id} supprimé avec succès par {user.email}")
        print(f"Contrat {contrat_id} supprimé avec succès.")
    except Contrat.DoesNotExist:
        logger.error(f"Tentative de suppression d'un contrat inexistant: {contrat_id}")
        print("\033[91mContrat non trouvé.\033[0m")


def gerer_contrats(current_user):
    logger = logging.getLogger(__name__)
    logger.info(f"Entrée dans la gestion des contrats par {current_user.email}")

    while True:
        print("\n\033[38;5;202mGestion des Contrats\033[0m\n")
        print("1. Liste de tous les contrats")
        print("2. Créer un nouveau contrat")
        print("3. Modifier un contrat")
        print("4. Supprimer un contrat")
        print("5. Réaffecter un contrat")
        print("6. Afficher les contrats non signés")
        print("7. Afficher les contrats non entièrement payés")
        print("8. Revenir au menu principal\n")

        choix = input("\033[96mChoisissez une action:\033[0m")
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
            logger.info("Sortie de la gestion des contrats")
            break
        else:
            logger.warning("Choix invalide dans la gestion des contrats")
            print("\033\n[91mChoix invalide. Veuillez réessayer.\033\n[0m")
