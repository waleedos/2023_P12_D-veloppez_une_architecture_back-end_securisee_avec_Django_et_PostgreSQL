import logging
import re
from epic_events_app.models import Evenement
from epic_auth_app.models import Utilisateur
from prettytable import PrettyTable
from epic_contracts_app.models import Contrat
from datetime import datetime
from django.utils.timezone import make_aware

logger = logging.getLogger(__name__)


def validate_name(name):
    if not re.fullmatch(r'^[A-Za-z\s]+$', name):
        raise ValueError("Le nom doit contenir uniquement des caractères alphabétiques et des espaces.")
    return name


def validate_attendees(input_str):
    try:
        attendees = int(input_str)
        if 0 <= attendees <= 9999:
            return attendees
        else:
            raise ValueError("Le nombre d'invités doit être compris entre 0 et 9999.")
    except ValueError:
        raise ValueError("Entrée invalide. Veuillez entrer un nombre valide pour les invités.")


def validate_notes(note):
    if len(note) > 350:
        raise ValueError("La note ne peut pas dépasser 350 caractères.")
    return note


def create_event(current_user):
    if current_user.department not in ['COM', 'ADM']:
        print("\n\033[91mAccès refusé. Seuls les utilisateurs COM et ADM peuvent créer des événements.\033\n[0m")
        return

    contrat_id = input("Entrez l'ID du contrat associé : ")

    try:
        contrat = Contrat.objects.get(id=contrat_id)
        if current_user.department != 'ADM' and contrat.statut != 'ACTIF':
            print(f"\n\033[91mLe contrat N° {contrat_id} du client {contrat.client.full_name} a le statut {contrat.statut}.\033\n[0m")
            return
        if current_user.department == 'COM' and current_user.id != contrat.client.commercial_assigne.id:
            print("\n\033[91mVous ne pouvez pas créer d'événement pour un client qui n'est pas le vôtre.\033\n[0m")
            return
    except Contrat.DoesNotExist:
        print("\n\033[91mContrat non trouvé.\033\n[0m")
        return

    try:
        nom = validate_name(input("Entrez le nom de l'événement : "))
        lieu = input("Location (adresse exacte de l'événement) : ")
        nombre_invites = validate_attendees(input("Attendees (nombre d'invités, max. 9999) : "))
        note = validate_notes(input("NOTE (max. 350 caractères) : "))
        type_evenement = input("Entrez le type de l'événement : ")

        date_debut_str = input("Entrez la date de début (format YYYY-MM-DD HH:MM) : ")
        try:
            date_debut = make_aware(datetime.strptime(date_debut_str, '%Y-%m-%d %H:%M'))
        except ValueError:
            print("\n\033[91mFormat de date de début invalide.\033\n[0m")
            return

        date_fin_str = input("Entrez la date de fin (format YYYY-MM-DD HH:MM) : ")
        try:
            date_fin = make_aware(datetime.strptime(date_fin_str, '%Y-%m-%d %H:%M'))
        except ValueError:
            print("\n\033[91mFormat de date de fin invalide.\033\n[0m")
            return

        evenement = Evenement(
            nom=nom, contrat=contrat, date_debut=date_debut, date_fin=date_fin,
            lieu=lieu, type_evenement=type_evenement, statut=Evenement.Statut.PLANIFIE,
            gestionnaire=None, nombre_invites=int(nombre_invites), note=note
        )
        evenement.save()
        print(f"\n\033[92mÉvénement '{nom}' créé avec succès.\033\n[0m")

    except ValueError as e:
        print(f"\n\033[91mErreur : {e}\033\n[0m")
        return
    except Exception as e:
        print(f"\n\033[91mUne erreur s'est produite : {e}\033\n[0m")
        return


def list_events(current_user):
    # Vérification des permissions de l'utilisateur
    if current_user.department in ['GES', 'ADM', 'SUP', 'COM']:
        events = Evenement.objects.all()
    else:
        events = Evenement.objects.filter(gestionnaire=current_user)

    if events.exists():
        table = PrettyTable()
        table.field_names = [
            " ID ", " Nom ", " Début ", " Fin ", " Lieu ", " Type ", " Statut ", " Contrat ID ", " Gestionnaire "
        ]
        table.border = False
        table.header = True
        table.align = 'l'

        for event in events:
            gestionnaire_email = event.gestionnaire.email if event.gestionnaire else 'N/A'
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

        # Calcul de la largeur maximale pour l'affichage
        max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
        border_line = '\033[38;5;128m╠' + '═' * (max_width - 2) + '╣\033[0m'  # Couleur violet

        # Affichage du tableau avec les bordures personnalisées et en violet
        print('\033[38;5;128m╔' + '═' * (max_width - 2) + '╗\033[0m')  # Couleur violet
        for i, line in enumerate(table.get_string().split("\n")):
            print('\033[38;5;128m║' + line.ljust(max_width - 2) + '║\033[0m')  # Couleur violet
            if i == 0:
                print(border_line)
        print('\033[38;5;128m╚' + '═' * (max_width - 2) + '╝\033[0m')  # Couleur violet
    else:
        print("\n\033[93mAucun événement disponible.\033[0m")


def update_event(current_user):
    print(f"Utilisateur actuel: {current_user.email}, Département: {current_user.department}")
    if current_user.department not in ['GES', 'SUP', 'ADM']:
        print("\n\033[93mAccès refusé. Seuls les utilisateurs GES et ADM peuvent modifier des événements.\033\n[0m")
        return

    event_id = input("Entrez l'ID de l'événement à modifier : ")
    try:
        evenement = Evenement.objects.get(id=event_id)
    except Evenement.DoesNotExist:
        print("\n\033[91mÉvénement non trouvé.\033\n[0m")
        return

    try:
        nom = validate_name(input("Entrez le nouveau nom de l'événement (laissez vide pour ne pas changer) : "))
        if nom:
            evenement.nom = nom

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
            try:
                evenement.date_debut = make_aware(datetime.strptime(date_debut_str, '%Y-%m-%d %H:%M'))
            except ValueError:
                print("\n\033[91mFormat de date de début invalide.\033N[0m")
                return

        date_fin_str = input("Entrez la nouvelle date de fin (YYYY-MM-DD HH:MM, laissez vide pour ne pas changer) : ")
        if date_fin_str:
            try:
                evenement.date_fin = make_aware(datetime.strptime(date_fin_str, '%Y-%m-%d %H:%M'))
            except ValueError:
                print("\n\033[91mFormat de date de fin invalide.\033\n[0m")
                return

        evenement.save()
        print(f"\n\033[92mÉvénement '{evenement.nom}' mis à jour avec succès.\033\n[0m")

    except ValueError as e:
        print(f"\n\033[91mErreur : {e}\033\n[0m")
        return
    except Exception as e:
        print(f"\n\033[91mUne erreur s'est produite : {e}\033\n[0m")
        return


def delete_event(current_user):
    if current_user.department not in ['GES', 'ADM']:
        print("\n\033[91mAccès refusé. Vous n’êtes ni GES ni ADM pour supprimer des événements.\033[0m\n")
        return

    try:
        event_id = input("Entrez l'ID de l'événement à supprimer : ").strip()
        evenement = Evenement.objects.get(id=event_id)
        confirmation = input(f"Êtes-vous sûr de vouloir supprimer l'événement '{evenement.nom}' ? (oui/non) : ").strip().lower()

        if confirmation == 'oui':
            evenement.delete()
            print(f"\n\033[92mÉvénement '{evenement.nom}' supprimé avec succès.\033\n[0m")
        else:
            print("\n\033[94mSuppression annulée.\033\n[0m")

    except Evenement.DoesNotExist:
        print("\n\033[91mÉvénement non trouvé.\033\n[0m")
    except Exception as e:
        print(f"\n\033[91mUne erreur s'est produite : {e}\033\n[0m")


def reassign_event(current_user):
    if current_user.department not in ['GES', 'ADM']:
        print("\n\033[91mAccès refusé. Vous n’êtes ni GES ni ADM pour réaffecter des événements.\033[0m\n")
        return

    try:
        event_id = input("Entrez l'ID de l'événement à réaffecter : ").strip()
        evenement = Evenement.objects.get(id=event_id)
        new_user_id = input("Entrez l'ID du nouvel utilisateur : ").strip()

        new_user = Utilisateur.objects.get(id=new_user_id)
        evenement.gestionnaire = new_user
        evenement.save()
        print(f"\n\033[92mL'événement '{evenement.nom}' a été réaffecté à l'utilisateur '{new_user.email}'.\033[0m")

    except Evenement.DoesNotExist:
        print("\n\033[91mÉvénement non trouvé.\033\n[0m")
    except Utilisateur.DoesNotExist:
        print("\n\033[91mUtilisateur non trouvé.\033\n[0m")
    except Exception as e:
        print(f"\n\033[91mUne erreur s'est produite : {e}\033\n[0m")


def gerer_events(current_user):
    while True:
        print("\n\033[38;5;202mGestion des Événements\033[0m\n")
        print("1. Lister les événements")
        print("2. Créer un nouvel événement")
        print("3. Modifier un événement")
        print("4. Supprimer un événement")
        print("5. Réaffecter un événement")
        print("6. Retourner au menu principal")

        choix = input("Choisissez une option: ")

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
        elif choix == '6':
            break
        else:
            print("\n\033[91mChoix invalide. Veuillez réessayer.\033\n[0m")
