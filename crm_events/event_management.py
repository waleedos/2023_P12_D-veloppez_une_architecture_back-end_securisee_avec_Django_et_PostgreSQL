from epic_events_app.models import Evenement
from epic_auth_app.models import Utilisateur
from prettytable import PrettyTable
from epic_contracts_app.models import Contrat
from datetime import datetime
from django.utils import timezone


def create_event(current_user):
    # Vérifier si l'utilisateur est autorisé
    if current_user.department not in ['COM', 'ADM']:
        print("\033[91mAccès refusé. Seuls les utilisateurs des départements "
              "GES et ADM peuvent créer des événements.\033[0m")
        return

    # Demander des informations sur l'événement
    nom = input("Entrez le nom de l'événement : ")
    contrat_id = input("Entrez l'ID du contrat associé : ")

    # Trouver le contrat associé
    try:
        contrat = Contrat.objects.get(id=contrat_id)
    except Contrat.DoesNotExist:
        print("Contrat non trouvé.")
        return

    # Demander d'autres informations
    date_debut_str = input("Entrez la date de début (format YYYY-MM-DD HH:MM) : ")
    date_fin_str = input("Entrez la date de fin (format YYYY-MM-DD HH:MM) : ")
    lieu = input("Entrez le lieu de l'événement : ")
    type_evenement = input("Entrez le type de l'événement : ")

    # Convertir les chaînes de date en objets datetime
    date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d %H:%M')
    date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d %H:%M')

    # Créer et enregistrer l'événement
    evenement = Evenement(
        nom=nom,
        contrat=contrat,
        date_debut=date_debut,
        date_fin=date_fin,
        lieu=lieu,
        type_evenement=type_evenement,
        statut=Evenement.Statut.PLANIFIE
    )
    evenement.save()
    print(f"Événement '{nom}' créé avec succès.")


def list_events(current_user):
    # Vérifier les permissions de l'utilisateur
    if current_user.department in ['GES', 'ADM', 'SUP', 'COM']:
        events = Evenement.objects.all()
    else:
        events = Evenement.objects.filter(gestionnaire=current_user)

    if events.exists():
        table = PrettyTable()
        table.field_names = ["ID", "Nom", "Début", "Fin", "Lieu", "Type", "Statut", "Contrat ID", "Gestionnaire"]
        table.border = False
        table.header = True
        table.align = 'l'

        for event in events:
            table.add_row([
                " " + str(event.id) + " ",
                " " + event.nom + " ",
                " " + event.date_debut.strftime('%Y-%m-%d %H:%M') + " ",
                " " + event.date_fin.strftime('%Y-%m-%d %H:%M') + " ",
                " " + event.lieu + " ",
                " " + event.type_evenement + " ",
                " " + event.statut + " ",
                " " + str(event.contrat.id) if event.contrat else 'N/A' + " ",
                " " + event.gestionnaire.email if event.gestionnaire else 'N/A' + " "
            ])

        # Calcul de la largeur maximale pour l'affichage
        max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
        border_line = '\033[92m╠' + '═' * (max_width - 2) + '╣\033[0m'

        # Affichage du tableau avec les bordures personnalisées et en orange
        print('\033[92m╔' + '═' * (max_width - 2) + '╗\033[0m')
        for i, line in enumerate(table.get_string().split("\n")):
            print('\033[92m║' + line.ljust(max_width - 2) + '║\033[0m')
            if i == 0:
                print(border_line)
        print('\033[92m╚' + '═' * (max_width - 2) + '╝\033[0m')
    else:
        print("\033[93mAucun événement disponible.\033[0m")


def update_event(current_user):
    print(f"Utilisateur actuel: {current_user.email}, Département: {current_user.department}")
    if current_user.department not in ['GES', 'SUP', 'ADM']:
        print("Accès refusé. Seuls les utilisateurs des départements GES et ADM peuvent modifier des événements.")
        return

    print("Événements disponibles dans la base de données :")
    for event in Evenement.objects.all():
        print(f"ID: {event.id}, Nom: {event.nom}")

    event_id = input("Entrez l'ID de l'événement à modifier : ")
    print(f"ID d'événement reçu: {event_id}")

    try:
        evenement = Evenement.objects.get(id=event_id)
        print(f"Événement trouvé: {evenement.nom}")
    except Evenement.DoesNotExist:
        print("Événement non trouvé.")
        return

    nom = input("Entrez le nouveau nom de l'événement (laissez vide pour ne pas changer) : ")
    if nom:
        print(f"Mise à jour du nom: {nom}")
        evenement.nom = nom

    date_debut_str = input(
        "Entrez la nouvelle date de début (format YYYY-MM-DD HH:MM, laissez vide pour ne pas changer) : "
    )

    if date_debut_str:
        evenement.date_debut = timezone.datetime.strptime(date_debut_str, '%Y-%m-%d %H:%M')
        print(f"Nouvelle date de début: {evenement.date_debut}")

    date_fin_str = input("Entrez la nouvelle date de fin (format YYYY-MM-DD HH:MM, laissez vide pour ne pas changer) : ")
    if date_fin_str:
        evenement.date_fin = timezone.datetime.strptime(date_fin_str, '%Y-%m-%d %H:%M')
        print(f"Nouvelle date de fin: {evenement.date_fin}")

    lieu = input("Entrez le nouveau lieu de l'événement (laissez vide pour ne pas changer) : ")
    if lieu:
        print(f"Nouveau lieu: {lieu}")
        evenement.lieu = lieu

    type_evenement = input("Entrez le nouveau type de l'événement (laissez vide pour ne pas changer) : ")
    if type_evenement:
        print(f"Nouveau type d'événement: {type_evenement}")
        evenement.type_evenement = type_evenement

    evenement.save()
    print(f"Événement '{evenement.nom}' mis à jour avec succès.")


def delete_event(current_user):
    # Vérifier si l'utilisateur est autorisé
    if current_user.department not in ['GES', 'ADM']:
        print("Accès refusé. Seuls les utilisateurs des départements GES et ADM peuvent supprimer des événements.")
        return

    # Demander l'ID de l'événement à supprimer
    event_id = input("Entrez l'ID de l'événement à supprimer : ")

    # Trouver l'événement associé
    try:
        evenement = Evenement.objects.get(id=event_id)
    except Evenement.DoesNotExist:
        print("Événement non trouvé.")
        return

    # Demander confirmation
    confirmation = input(f"Êtes-vous sûr de vouloir supprimer l'événement '{evenement.nom}' ? (oui/non) : ")
    if confirmation.lower() == 'oui':
        evenement.delete()
        print(f"Événement '{evenement.nom}' supprimé avec succès.")
    else:
        print("Suppression annulée.")


def reassign_event(current_user):
    # Vérifier si l'utilisateur est autorisé
    if current_user.department not in ['GES', 'ADM']:
        print("Accès refusé. Seuls les utilisateurs des départements GES et ADM peuvent réaffecter des événements.")
        return

    # Demander l'ID de l'événement à réaffecter
    event_id = input("Entrez l'ID de l'événement à réaffecter : ")

    # Trouver l'événement associé
    try:
        evenement = Evenement.objects.get(id=event_id)
    except Evenement.DoesNotExist:
        print("Événement non trouvé.")
        return

    # Demander l'ID du nouvel utilisateur
    new_user_id = input("Entrez l'ID du nouvel utilisateur (gestionnaire ou contact commercial) : ")

    # Trouver le nouvel utilisateur
    try:
        new_user = Utilisateur.objects.get(id=new_user_id)
    except Utilisateur.DoesNotExist:
        print("Utilisateur non trouvé.")
        return

    # Réaffecter l'événement et sauvegarder
    evenement.gestionnaire = new_user
    evenement.save()

    print(f"L'événement '{evenement.nom}' a été réaffecté à l'utilisateur '{new_user.email}'.")


def gerer_events(current_user):
    while True:
        # Affichage des options disponibles
        print("\n\033[38;5;202mGestion des Événements\033[0m\n")
        print("1. Lister les événements")
        print("2. Créer un nouvel événement")
        print("3. Modifier un événement")
        print("4. Supprimer un événement")
        print("5. Réaffecter un événement")
        print("6. Retourner au menu principal")

        choix = input("Choisissez une option: ")

        # Exécuter la fonction correspondante en fonction du choix
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
            print("Choix invalide. Veuillez réessayer.")
