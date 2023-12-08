import logging
import re
from epic_events_app.models import Evenement
from epic_auth_app.models import Utilisateur
from prettytable import PrettyTable
from epic_contracts_app.models import Contrat
from datetime import datetime
from django.utils.timezone import make_aware
from filtres import filtrer_evenements_sans_support, afficher_evenements


logger = logging.getLogger(__name__)


def validate_name(name, updating=False):
    # Permettre de laisser le champ vide si c'est une mise à jour et que le nom n'est pas fourni.
    if updating and not name:
        return None
    # Vérifier si le nom ne contient que des caractères alphabétiques et des espaces.
    if not re.fullmatch(r'^[A-Za-z\s]+$', name):
        # Lever une exception si le nom ne respecte pas le format requis.
        raise ValueError("Le nom doit contenir uniquement des caractères alphabétiques et des espaces.")
    # Retourner le nom si celui-ci est valide.
    return name


def validate_attendees(input_str):
    try:
        # Convertir la chaîne de caractères d'entrée en entier.
        attendees = int(input_str)
        # Vérifier si le nombre d'invités est dans la plage autorisée (0 à 9999).
        if 0 <= attendees <= 9999:
            return attendees
        else:
            # Lever une exception si le nombre d'invités n'est pas dans la plage autorisée.
            raise ValueError("Le nombre d'invités doit être compris entre 0 et 9999.")
    except ValueError:
        # Lever une exception si l'entrée n'est pas un nombre valide.
        raise ValueError("Entrée invalide. Veuillez entrer un nombre valide pour les invités.")


def validate_notes(note):
    # Vérifier si la longueur de la note dépasse 350 caractères.
    if len(note) > 350:
        # Lever une exception si la note est trop longue.
        raise ValueError("La note ne peut pas dépasser 350 caractères.")
    # Retourner la note si elle est valide.
    return note


# Définir la fonction `create_event` qui prend en paramètre `current_user`
def create_event(current_user):
    # Configurer un logger pour enregistrer les informations et erreurs
    logger = logging.getLogger(__name__)
    # Enregistrer dans le logger une information sur la tentative de création d'événement
    logger.info(f"Tentative de création d'un événement par {current_user.email}")

    # Vérifier si l'utilisateur actuel appartient aux départements autorisés
    if current_user.department not in ['COM', 'ADM']:
        # Enregistrer un avertissement dans le logger en cas d'utilisateur non autorisé
        logger.warning("Accès refusé à la création d'événement - Utilisateur non autorisé")
        # Afficher un message d'erreur à l'utilisateur
        print("\n\033[91mAccès refusé. Seuls les utilisateurs COM et ADM peuvent créer des événements.\033\n[0m")
        return  # Terminer la fonction si l'utilisateur n'est pas autorisé

    # Demander à l'utilisateur d'entrer l'ID du contrat associé
    contrat_id = input("Entrez l'ID du contrat associé : ")

    try:
        # Tenter de récupérer le contrat à partir de l'ID fourni
        contrat = Contrat.objects.get(id=contrat_id)
        # Vérifier les conditions spécifiques au département de l'utilisateur et au statut du contrat
        if current_user.department != 'ADM' and contrat.statut != 'ACTIF':
            # Enregistrer un avertissement dans le logger si le contrat n'est pas actif
            logger.warning(f"Contrat non actif pour la création de l'événement: {contrat_id}")
            # Afficher un message d'erreur à l'utilisateur
            print(f"\n\033[91mLe contrat N° {contrat_id} a le statut {contrat.statut}.\033\n[0m")
            return
        if current_user.department == 'COM' and current_user.id != contrat.client.commercial_assigne.id:
            # Enregistrer un avertissement dans le logger si le commercial assigné ne correspond pas
            logger.warning(f"Tentative de création d'événement pour un client non assigné: {contrat.client.full_name}")
            # Afficher un message d'erreur à l'utilisateur
            print("\n\033[91mVous ne pouvez pas créer d'événement pour un client qui n'est pas le vôtre.\033\n[0m")
            return
    except Contrat.DoesNotExist:
        # Enregistrer une erreur dans le logger si le contrat n'est pas trouvé
        logger.error(f"Contrat non trouvé pour la création de l'événement: {contrat_id}")
        # Afficher un message d'erreur à l'utilisateur
        print("\n\033[91mContrat non trouvé.\033\n[0m")
        return  # Terminer la fonction si le contrat n'existe pas

    try:
        # Demander les détails de l'événement et valider les entrées
        nom = validate_name(input("Entrez le nom de l'événement : "))
        lieu = input("Location (adresse exacte de l'événement) : ")
        nombre_invites = validate_attendees(input("Attendees (nombre d'invités, max. 9999) : "))
        note = validate_notes(input("NOTE (max. 350 caractères) : "))
        type_evenement = input("Entrez le type de l'événement : ")

        # Demander et traiter les dates de début et de fin de l'événement
        date_debut_str = input("Entrez la date de début (format YYYY-MM-DD HH:MM) : ")
        date_debut = make_aware(datetime.strptime(date_debut_str, '%Y-%m-%d %H:%M'))
        date_fin_str = input("Entrez la date de fin (format YYYY-MM-DD HH:MM) : ")
        date_fin = make_aware(datetime.strptime(date_fin_str, '%Y-%m-%d %H:%M'))

        # Créer un nouvel objet Evenement avec les informations fournies
        evenement = Evenement(
            nom=nom, contrat=contrat, date_debut=date_debut, date_fin=date_fin,
            lieu=lieu, type_evenement=type_evenement, statut=Evenement.Statut.PLANIFIE,
            gestionnaire=None, nombre_invites=nombre_invites, note=note
        )
        # Sauvegarder l'objet Evenement dans la base de données
        evenement.save()
        # Enregistrer dans le logger la réussite de la création de l'événement
        logger.info(f"Événement '{nom}' créé avec succès")
        # Afficher un message de succès à l'utilisateur
        print(f"\n\033[92mÉvénement '{nom}' créé avec succès.\033\n[0m")
    except ValueError as e:
        # Enregistrer une erreur dans le logger et afficher un message en cas d'erreur de valeur
        logger.error(f"Erreur lors de la création de l'événement: {e}")
        print(f"\n\033[91mErreur : {e}\033\n[0m")
    except Exception as e:
        # Enregistrer une erreur dans le logger et afficher un message en cas d'erreur inattendue
        logger.error(f"Une erreur s'est produite lors de la création de l'événement: {e}")
        print(f"\n\033[91mUne erreur s'est produite : {e}\033\n[0m")


# Définir la fonction `list_events` qui prend en paramètre `current_user`
def list_events(current_user):
    # Configurer un logger pour enregistrer les informations et erreurs
    logger = logging.getLogger(__name__)
    # Enregistrer dans le logger une information sur la tentative d'affichage des événements
    logger.info(f"Tentative d'affichage des événements par {current_user.email}")

    # Vérifier le département de l'utilisateur pour déterminer les événements à afficher
    if current_user.department == 'SUP':
        # Récupérer les événements gérés par l'utilisateur si celui-ci est du département SUP
        events = Evenement.objects.filter(gestionnaire=current_user)
    elif current_user.department in ['GES', 'ADM', 'COM']:
        # Récupérer tous les événements si l'utilisateur appartient à l'un de ces départements
        events = Evenement.objects.all()
    else:
        # Enregistrer un avertissement dans le logger en cas d'accès non autorisé
        logger.warning("Accès refusé à l'affichage des événements - Utilisateur non autorisé")
        # Afficher un message d'erreur à l'utilisateur
        print("\n\033[91mAccès refusé. Vous n'avez pas l'autorisation nécessaire.\033[0m")
        return  # Terminer la fonction si l'utilisateur n'est pas autorisé

    # Vérifier si des événements existent dans la base de données
    if events.exists():
        # Créer un tableau pour afficher les événements
        table = PrettyTable()
        # Définir les en-têtes du tableau
        table.field_names = [
            " ID ", " Nom ", " Début ", " Fin ", " Lieu ", " Type ",
            " Statut ", " Contrat ID ", " Gestionnaire "
        ]
        # Configurer l'affichage du tableau
        table.border = False
        table.header = True
        table.align = 'l'

        # Parcourir chaque événement et ajouter une ligne dans le tableau
        for event in events:
            # Récupérer l'email du gestionnaire s'il existe, sinon mettre 'N/A'
            gestionnaire_email = event.gestionnaire.email if event.gestionnaire else 'N/A'
            # Ajouter une ligne au tableau avec les détails de l'événement
            table.add_row([
                " " + str(event.id) + " ",
                " " + event.nom + " ",
                " " + event.date_debut.strftime('%Y-%m-%d %H:%M') + " ",
                " " + event.date_fin.strftime('%Y-%m-%d %H:%M') + " ",
                " " + event.lieu + " ",
                " " + event.type_evenement + " ",
                " " + event.statut + " ",
                " " + str(event.contrat.id) if event.contrat else 'N/A',
                " " + gestionnaire_email + " "
            ])

        # Calculer la largeur maximale du tableau pour l'affichage
        max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
        # Créer une ligne de bordure pour le tableau
        border_line = '\033[38;5;128m╠' + '═' * (max_width - 2) + '╣\033[0m'

        # Afficher le tableau avec des bordures et des couleurs
        print('\033[38;5;128m╔' + '═' * (max_width - 2) + '╗\033[0m')
        for i, line in enumerate(table.get_string().split("\n")):
            print('\033[38;5;128m║' + line.ljust(max_width - 2) + '║\033[0m')
            if i == 0:
                print(border_line)
        print('\033[38;5;128m╚' + '═' * (max_width - 2) + '╝\033[0m')
        # Enregistrer dans le logger que les événements ont été affichés avec succès
        logger.info("Événements affichés avec succès")
    else:
        # Enregistrer un avertissement dans le logger si aucun événement n'est disponible
        logger.warning("Aucun événement disponible à afficher")
        # Afficher un message indiquant qu'aucun événement n'est disponible
        print("\n\033[93mAucun événement disponible.\033[0m")


# Définir la fonction `update_event` pour la mise à jour d'un événement
def update_event(current_user):
    # Configurer un logger pour enregistrer les informations et erreurs
    logger = logging.getLogger(__name__)
    # Enregistrer dans le logger une information sur la tentative de mise à jour d'un événement
    logger.info(f"Tentative de mise à jour d'un événement par {current_user.email}")

    # Vérifier si l'utilisateur actuel est autorisé à mettre à jour des événements
    if current_user.department not in ['GES', 'SUP', 'ADM']:
        # Enregistrer un avertissement dans le logger en cas d'accès non autorisé
        logger.warning(f"Accès refusé pour la mise à jour d'événement par {current_user.email}")
        # Afficher un message d'erreur à l'utilisateur
        print("\n\033[93mAccès refusé. Seuls les utilisateurs GES et ADM peuvent modifier des événements.\033\n[0m")
        return  # Terminer la fonction si l'utilisateur n'est pas autorisé

    # Demander à l'utilisateur de saisir l'ID de l'événement à modifier
    event_id = input("Entrez l'ID de l'événement à modifier : ")
    try:
        # Tenter de récupérer l'événement à partir de l'ID fourni
        evenement = Evenement.objects.get(id=event_id)
    except Evenement.DoesNotExist:
        # Enregistrer une erreur dans le logger si l'événement n'est pas trouvé
        logger.error(f"Événement non trouvé pour l'ID: {event_id}")
        # Afficher un message d'erreur à l'utilisateur
        print("\n\033[91mÉvénement non trouvé.\033\n[0m")
        return

    try:
        # Demander et mettre à jour les différents attributs de l'événement
        nom = input("Entrez le nouveau nom de l'événement (laissez vide pour ne pas changer) : ")
        if nom:
            evenement.nom = validate_name(nom, updating=True)

        lieu = input("Entrez le nouveau lieu de l'événement (laissez vide pour ne pas changer) : ")
        if lieu:
            evenement.lieu = lieu

        nombre_invites_str = input("Entrez le nombre d'invités (max. 9999, laissez vide pour ne pas changer) : ")
        if nombre_invites_str:
            evenement.nombre_invites = int(validate_attendees(nombre_invites_str))

        note = input("Entrez la note (max. 350 caractères, laissez vide pour ne pas changer) : ")
        if note:
            evenement.note = validate_notes(note)

        type_evenement = input("Entrez le nouveau type de l'événement (laissez vide pour ne pas changer) : ")
        if type_evenement:
            evenement.type_evenement = type_evenement

        date_debut_str = input("Entrez la nouvelle date de début (YYYY-MM-DD HH:MM, laissez vide pour ne pas changer) : ")
        if date_debut_str:
            evenement.date_debut = make_aware(datetime.strptime(date_debut_str, '%Y-%m-%d %H:%M'))

        date_fin_str = input("Entrez la nouvelle date de fin (YYYY-MM-DD HH:MM, laissez vide pour ne pas changer) : ")
        if date_fin_str:
            evenement.date_fin = make_aware(datetime.strptime(date_fin_str, '%Y-%m-%d %H:%M'))

        # Sauvegarder les modifications apportées à l'événement
        evenement.save()
        # Enregistrer dans le logger la réussite de la mise à jour de l'événement
        logger.info(f"Événement '{evenement.nom}' mis à jour avec succès")
        # Afficher un message de succès à l'utilisateur
        print(f"\n\033[92mÉvénement '{evenement.nom}' mis à jour avec succès.\033\n[0m")
    except ValueError as e:
        # Enregistrer une erreur dans le logger et afficher un message en cas d'erreur de valeur
        logger.error(f"Erreur lors de la mise à jour de l'événement: {e}")
        print(f"\n\033[91mErreur : {e}\033\n[0m")
    except Exception as e:
        # Enregistrer une erreur dans le logger et afficher un message en cas d'erreur inattendue
        logger.error(f"Une erreur inattendue s'est produite lors de la mise à jour de l'événement: {e}")
        print(f"\n\033[91mUne erreur s'est produite : {e}\033\n[0m")


# Définir la fonction `delete_event` qui prend en paramètre `current_user`
def delete_event(current_user):
    # Vérifier si l'utilisateur actuel est autorisé à supprimer des événements
    if current_user.department not in ['GES', 'ADM']:
        # Afficher un message d'erreur si l'utilisateur n'est pas autorisé
        print("\n\033[91mAccès refusé. Vous n’êtes ni GES ni ADM pour supprimer des événements.\033[0m\n")
        return  # Terminer la fonction si l'utilisateur n'est pas autorisé

    try:
        # Demander à l'utilisateur de saisir l'ID de l'événement à supprimer
        event_id = input("Entrez l'ID de l'événement à supprimer : ").strip()
        # Tenter de récupérer l'événement à partir de l'ID fourni
        evenement = Evenement.objects.get(id=event_id)
        # Demander une confirmation de suppression à l'utilisateur
        confirmation = input(
            f"Êtes-vous sûr de vouloir supprimer l'événement '{evenement.nom}' ? "
            "(oui/non) : "
        ).strip().lower()

        # Vérifier si l'utilisateur confirme la suppression
        if confirmation == 'oui':
            # Supprimer l'événement de la base de données
            evenement.delete()
            # Afficher un message de confirmation de suppression
            print(f"\n\033[92mÉvénement '{evenement.nom}' supprimé avec succès.\033\n[0m")
        else:
            # Afficher un message indiquant l'annulation de la suppression
            print("\n\033[94mSuppression annulée.\033\n[0m")

    except Evenement.DoesNotExist:
        # Afficher un message d'erreur si l'événement n'est pas trouvé
        print("\n\033[91mÉvénement non trouvé.\033\n[0m")
    except Exception as e:
        # Afficher un message d'erreur en cas d'exception non gérée
        print(f"\n\033[91mUne erreur s'est produite : {e}\033\n[0m")


# Définir la fonction `reassign_event` pour réaffecter un événement
def reassign_event(current_user):
    # Vérifier si l'utilisateur actuel est autorisé à réaffecter des événements
    if current_user.department not in ['GES', 'ADM']:
        # Afficher un message d'erreur si l'utilisateur n'est pas autorisé
        print("\n\033[91mAccès refusé. Vous n’êtes ni GES ni ADM pour réaffecter des événements.\033[0m\n")
        return  # Terminer la fonction si l'utilisateur n'est pas autorisé

    try:
        # Demander à l'utilisateur de saisir l'ID de l'événement à réaffecter
        event_id = input("Entrez l'ID de l'événement à réaffecter : ").strip()
        # Tenter de récupérer l'événement à partir de l'ID fourni
        evenement = Evenement.objects.get(id=event_id)
        # Demander à l'utilisateur de saisir l'ID du nouvel utilisateur
        new_user_id = input("Entrez l'ID du nouvel utilisateur : ").strip()

        # Tenter de récupérer le nouvel utilisateur à partir de l'ID fourni
        new_user = Utilisateur.objects.get(id=new_user_id)
        # Affecter le nouvel utilisateur comme gestionnaire de l'événement
        evenement.gestionnaire = new_user
        # Sauvegarder les modifications apportées à l'événement
        evenement.save()
        # Afficher un message confirmant la réaffectation de l'événement
        print(f"\n\033[92mL'événement '{evenement.nom}' a été réaffecté à l'utilisateur '{new_user.email}'.\033[0m")

    except Evenement.DoesNotExist:
        # Afficher un message d'erreur si l'événement n'est pas trouvé
        print("\n\033[91mÉvénement non trouvé.\033\n[0m")
    except Utilisateur.DoesNotExist:
        # Afficher un message d'erreur si l'utilisateur n'est pas trouvé
        print("\n\033[91mUtilisateur non trouvé.\033\n[0m")
    except Exception as e:
        # Afficher un message d'erreur en cas d'exception non gérée
        print(f"\n\033[91mUne erreur s'est produite : {e}\033\n[0m")


# Définir la fonction `gerer_events` pour gérer les opérations liées aux événements
def gerer_events(current_user):
    while True:
        # Afficher le menu des opérations liées aux événements
        print("\n\033[38;5;202mGestion des Événements\033[0m\n")
        print("1. Lister les événements")
        print("2. Créer un nouvel événement")
        print("3. Modifier un événement")
        print("4. Supprimer un événement")
        print("5. Réaffecter un événement")

        # Ajouter une option supplémentaire pour les utilisateurs du département GES
        if current_user.department == 'GES':
            print("6. Filtrer les événements sans support")

        print("7. Retourner au menu principal\n")

        # Demander à l'utilisateur de choisir une option
        choix = input("\033[96mChoisissez une option:\033[0m")

        # Exécuter la fonction correspondante en fonction du choix de l'utilisateur
        if choix == '1':
            list_events(current_user)
        elif choix == '2':
            create_event(current_user)
        elif choix == '3':
            update_event(current_user)
        elif choix == '4':
            delete_event(current_user)
        elif choix == '5':
            reassign_event(current_user)
        elif choix == '6' and current_user.department == 'GES':
            evenements = filtrer_evenements_sans_support()
            afficher_evenements(evenements)
        elif choix == '7':
            break  # Quitter la boucle et terminer la fonction
        else:
            # Afficher un message en cas de choix invalide
            print("\n\033[91mChoix invalide. Veuillez réessayer.\033\n[0m")
