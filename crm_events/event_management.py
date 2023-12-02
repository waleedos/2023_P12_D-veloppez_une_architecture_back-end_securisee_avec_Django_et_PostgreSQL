from epic_events_app.models import Evenement
from epic_auth_app.models import Utilisateur
from prettytable import PrettyTable
from epic_contracts_app.models import Contrat
from datetime import datetime


def create_event(current_user):
    # Vérifier si l'utilisateur est dans le département COMMERCIAL ou ADMINISTRATION
    if current_user.department not in ['COM', 'ADM']:
        print("\033[91mAccès refusé. Seuls les utilisateurs COM et ADM peuvent créer des événements.\033[0m")
        return

    # Collecte des informations sur l'événement
    nom = input("Entrez le nom de l'événement : ")
    contrat_id = input("Entrez l'ID du contrat associé : ")

    try:
        contrat = Contrat.objects.get(id=contrat_id)
        # Pour les utilisateurs non-ADM, vérifier si le contrat est signé
        if current_user.department != 'ADM' and not contrat.est_signe:
            print("\033[91mImpossible de créer un événement pour un contrat non signé.\033[0m")
            return
    except Contrat.DoesNotExist:
        print("\033[91mContrat non trouvé.\033[0m")
        return

    # Plus de détails sur l'événement
    date_debut_str = input("Entrez la date de début (format YYYY-MM-DD HH:MM) : ")
    date_fin_str = input("Entrez la date de fin (format YYYY-MM-DD HH:MM) : ")
    lieu = input("Entrez le lieu de l'événement : ")
    type_evenement = input("Entrez le type de l'événement : ")

    # Conversion des dates
    date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d %H:%M')
    date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d %H:%M')

    # Création de l'événement
    evenement = Evenement(
        nom=nom, contrat=contrat, date_debut=date_debut, date_fin=date_fin,
        lieu=lieu, type_evenement=type_evenement, statut=Evenement.Statut.PLANIFIE
    )
    evenement.save()
    print(f"\033[92mÉvénement '{nom}' créé avec succès.\033[0m")


def list_events(current_user):
    # Vérification des permissions de l'utilisateur
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
            gestionnaire_email = event.gestionnaire.email if event.gestionnaire else 'N/A'
            table.add_row([
                str(event.id), event.nom,
                event.date_debut.strftime('%Y-%m-%d %H:%M'),
                event.date_fin.strftime('%Y-%m-%d %H:%M'),
                event.lieu, event.type_evenement,
                event.statut,
                str(event.contrat.id) if event.contrat else 'N/A',
                gestionnaire_email
            ])

        # Affichage du tableau
        print(table)
    else:
        print("\033[93mAucun événement disponible.\033[0m")


def update_event(current_user):
    print(f"Utilisateur actuel: {current_user.email}, Département: {current_user.department}")
    if current_user.department not in ['GES', 'SUP', 'ADM']:
        print("Accès refusé. Seuls les utilisateurs GES et ADM peuvent modifier des événements.")
        return

    # Affichage des événements disponibles
    print("Événements disponibles dans la base de données :")
    for event in Evenement.objects.all():
        print(f"ID: {event.id}, Nom: {event.nom}")

    event_id = input("Entrez l'ID de l'événement à modifier : ")
    try:
        evenement = Evenement.objects.get(id=event_id)
        print(f"Événement trouvé: {evenement.nom}")
    except Evenement.DoesNotExist:
        print("\n\033[91mÉvénement non trouvé.\033[0m\n")
        return

    # Mise à jour des informations de l'événement
    nom = input("Entrez le nouveau nom de l'événement (laissez vide pour ne pas changer) : ")
    if nom:
        evenement.nom = nom

    date_debut_str = input("Entrez la nouvelle date de début (YYYY-MM-DD HH:MM) : ")
    if date_debut_str:
        evenement.date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d %H:%M')

    date_fin_str = input("Entrez la nouvelle date de fin (YYYY-MM-DD HH:MM) : ")
    if date_fin_str:
        evenement.date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d %H:%M')

    lieu = input("Entrez le nouveau lieu de l'événement : ")
    if lieu:
        evenement.lieu = lieu

    type_evenement = input("Entrez le nouveau type de l'événement : ")
    if type_evenement:
        evenement.type_evenement = type_evenement

    evenement.save()
    print(f"\033[92mÉvénement '{evenement.nom}' mis à jour avec succès.\033[0m")


def delete_event(current_user):
    if current_user.department not in ['GES', 'ADM']:
        print("\n\033[91mAccès refusé. Vous n’êtes ni GES ni ADM pour supprimer des événements.\033[0m\n")
        return

    event_id = input("Entrez l'ID de l'événement à supprimer : ")
    try:
        evenement = Evenement.objects.get(id=event_id)
    except Evenement.DoesNotExist:
        print("\n\033[91mÉvénement non trouvé.\033[0m\n")
        return

    confirmation = input(f"Êtes-vous sûr de vouloir supprimer l'événement '{evenement.nom}' ? (oui/non) : ")
    if confirmation.lower() == 'oui':
        evenement.delete()
        print(f"Événement '{evenement.nom}' supprimé avec succès.")
    else:
        print("\n\033[91mSuppression annulée.\033[0m\n")


def reassign_event(current_user):
    if current_user.department not in ['GES', 'ADM']:
        print("\n\033[91mAccès refusé. Vous n’êtes ni GES ni ADM pour réaffecter des événements.\033[0m\n")
        return

    event_id = input("Entrez l'ID de l'événement à réaffecter : ")
    try:
        evenement = Evenement.objects.get(id=event_id)
    except Evenement.DoesNotExist:
        print("\n\033[91mÉvénement non trouvé.\033[0m\n")
        return

    new_user_id = input("Entrez l'ID du nouvel utilisateur : ")
    try:
        new_user = Utilisateur.objects.get(id=new_user_id)
    except Utilisateur.DoesNotExist:
        print("\n\033[91mUtilisateur non trouvé.\033[0m\n")
        return

    evenement.gestionnaire = new_user
    evenement.save()
    print(f"\033[92mL'événement '{evenement.nom}' a été réaffecté à l'utilisateur '{new_user.email}'\033[0m")


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
            print("\033[91mChoix invalide. Veuillez réessayer.\033[0m")
