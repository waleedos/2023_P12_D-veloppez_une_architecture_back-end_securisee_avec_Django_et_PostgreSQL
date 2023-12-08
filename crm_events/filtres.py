# Importation des modèles nécessaires à partir de différentes applications
from epic_auth_app.models import Utilisateur
from epic_events_app.models import Evenement
from epic_contracts_app.models import Contrat
from prettytable import PrettyTable
import logging

# Configuration du logger pour enregistrer les informations de débogage
logger = logging.getLogger(__name__)


# Définition de la fonction pour filtrer les utilisateurs en fonction du code de département
def filtrer_utilisateurs_par_departement(departement_code):
    # Vérification si le code de département n'est pas 'AUT'
    if departement_code != 'AUT':
        # Retourner les utilisateurs dont le département correspond au code fourni
        return Utilisateur.objects.filter(department=departement_code)
    else:
        # Exclure les utilisateurs de certains départements (ADM, GES, COM, SUP) si le code est 'AUT'
        return Utilisateur.objects.exclude(department__in=['ADM', 'GES', 'COM', 'SUP'])


# Définition de la fonction pour afficher les informations des utilisateurs dans un tableau
def afficher_utilisateurs(utilisateurs):
    # Création d'un objet PrettyTable
    table = PrettyTable()
    # Définition des en-têtes du tableau
    table.field_names = ["ID", "Email", "Prénom", "Nom", "Département", "Superutilisateur"]
    # Désactivation des bordures du tableau
    table.border = False
    # Activation de l'en-tête du tableau
    table.header = True
    # Alignement des cellules du tableau à gauche
    table.align = 'l'

    # Vérification de l'existence d'utilisateurs
    if utilisateurs.exists():
        # Parcours des utilisateurs pour les ajouter au tableau
        for utilisateur in utilisateurs:
            table.add_row([
                " " + str(utilisateur.id) + " ",
                " " + utilisateur.email + " ",
                " " + utilisateur.first_name + " ",
                " " + utilisateur.last_name + " ",
                " " + utilisateur.department + " ",
                " Yes " if utilisateur.is_superuser else " No ",
            ])

        # Calcul de la largeur maximale pour l'affichage
        max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
        # Création d'une ligne de séparation avec une couleur spécifique
        border_line = '\033[94m╠' + '═' * (max_width - 2) + '╣\033[0m'
        # Code couleur ANSI pour un bleu clair
        light_blue_color_code = '\033[96m'

        # Affichage du haut du tableau avec la couleur spécifiée
        print(light_blue_color_code + '╔' + '═' * (max_width - 2) + '╗\033[0m')
        # Affichage des lignes du tableau avec la couleur spécifiée
        for i, line in enumerate(table.get_string().split("\n")):
            print(light_blue_color_code + '║' + line.ljust(max_width - 2) + '║\033[0m')
            # Affichage de la ligne de séparation après l'en-tête
            if i == 0:
                print(light_blue_color_code + border_line + '\033[0m')
        # Affichage du bas du tableau avec la couleur spécifiée
        print(light_blue_color_code + '╚' + '═' * (max_width - 2) + '╝\033[0m')
    else:
        # Affichage d'un message si aucun utilisateur n'est disponible
        print("\033[93mAucun utilisateur disponible.\033[0m")


# Définition de la fonction pour filtrer les événements qui n'ont pas de gestionnaire assigné
def filtrer_evenements_sans_support():
    # Retourner les événements pour lesquels l'attribut 'gestionnaire' est null, signifiant
    # qu'aucun gestionnaire n'est assigné
    return Evenement.objects.filter(gestionnaire__isnull=True)


# Définition de la fonction pour afficher les informations des événements dans un tableau
def afficher_evenements(evenements):
    # Création d'un objet PrettyTable
    table = PrettyTable()
    # Définition des en-têtes du tableau avec les noms des champs
    table.field_names = ["ID", "Nom", "Début", "Fin", "Lieu", "Type", "Statut", "Contrat ID", "Gestionnaire"]
    # Désactivation des bordures du tableau
    table.border = False
    # Activation de l'en-tête du tableau
    table.header = True
    # Alignement des cellules du tableau à gauche
    table.align = 'l'

    # Parcours de la liste des événements pour les ajouter au tableau
    for evenement in evenements:
        # Récupération de l'email du gestionnaire s'il existe, sinon 'N/A'
        gestionnaire_email = evenement.gestionnaire.email if evenement.gestionnaire else 'N/A'
        # Ajout des informations de chaque événement au tableau
        table.add_row([
            " " + str(evenement.id) + " ",
            " " + evenement.nom + " ",
            " " + evenement.date_debut.strftime('%Y-%m-%d %H:%M') + " ",
            " " + evenement.date_fin.strftime('%Y-%m-%d %H:%M') + " ",
            " " + evenement.lieu + " ",
            " " + evenement.type_evenement + " ",
            " " + evenement.statut + " ",
            " " + str(evenement.contrat.id) if evenement.contrat else 'N/A',
            " " + gestionnaire_email + " "
        ])

    # Calcul de la largeur maximale pour l'affichage
    max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
    # Code couleur ANSI pour un violet clair
    light_violet_color_code = '\033[95m'
    # Création d'une ligne de séparation de couleur violet clair
    border_line = light_violet_color_code + '╠' + '═' * (max_width - 2) + '╣\033[0m'

    # Affichage du haut du tableau avec la couleur spécifiée
    print(light_violet_color_code + '╔' + '═' * (max_width - 2) + '╗\033[0m')
    # Affichage des lignes du tableau avec la couleur spécifiée
    for i, line in enumerate(table.get_string().split("\n")):
        print(light_violet_color_code + '║' + line.ljust(max_width - 2) + '║\033[0m')
        # Affichage de la ligne de séparation après l'en-tête
        if i == 0:
            print(border_line)
    # Affichage du bas du tableau avec la couleur spécifiée
    print(light_violet_color_code + '╚' + '═' * (max_width - 2) + '╝\033[0m')


# Définition de la fonction pour filtrer les contrats qui n'ont pas encore été signés
def filtrer_contrats_non_signes():
    # Retourner les contrats dont le statut est 'EN_ATTENTE', signifiant qu'ils ne sont pas encore signés
    return Contrat.objects.filter(statut='EN_ATTENTE')


# Définition de la fonction pour filtrer les contrats qui n'ont pas été entièrement payés
def filtrer_contrats_non_entierement_payes():
    # Retourner les contrats dont le montant restant à payer est supérieur à 0
    return Contrat.objects.filter(montant_restant__gt=0)


# Définition de la fonction pour afficher les informations des contrats dans un tableau
def afficher_contrats(contrats):
    # Enregistrement d'un message d'information dans le logger
    logger.info("Affichage des contrats filtrés")

    # Vérification si aucun contrat ne correspond aux critères de filtrage
    if not contrats.exists():
        # Enregistrement d'un message d'avertissement dans le logger
        logger.warning("Aucun contrat correspondant aux critères pour l'affichage")
        # Affichage d'un message d'alerte indiquant l'absence de contrats correspondants
        print("\033[93mAucun contrat correspondant aux critères.\033[0m")
        # Fin de la fonction si aucun contrat n'est trouvé
        return

    # Création d'un objet PrettyTable pour l'affichage
    table = PrettyTable()
    # Définition des en-têtes du tableau
    table.field_names = [
        " ID ", " Nom ", " Client ", " Montant Total ", " Montant Restant ",
        " Date de Création ", " Statut ", " Client géré par (COM) "
    ]
    # Désactivation des bordures du tableau
    table.border = False
    # Activation de l'en-tête du tableau
    table.header = True
    # Alignement des cellules du tableau à gauche
    table.align = 'l'

    # Parcours de chaque contrat pour les ajouter au tableau
    for contrat in contrats:
        # Récupération du nom complet du commercial assigné au client, sinon 'N/A'
        commercial_assigne = (
            contrat.client.commercial_assigne.get_full_name()
            if contrat.client.commercial_assigne else 'N/A'
        )
        # Ajout des informations du contrat au tableau
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

    # Calcul de la largeur maximale pour l'affichage
    max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
    # Création d'une ligne de séparation avec une couleur spécifique
    border_line = '\033[38;5;202m╠' + '═' * (max_width - 2) + '╣\033[0m'

    # Affichage du haut du tableau avec la couleur spécifiée
    print('\033[38;5;202m╔' + '═' * (max_width - 2) + '╗\033[0m')
    # Affichage des lignes du tableau avec la couleur spécifiée
    for i, line in enumerate(table.get_string().split("\n")):
        print('\033[38;5;202m║' + line.ljust(max_width - 2) + '║\033[0m')
        # Affichage de la ligne de séparation après l'en-tête
        if i == 0:
            print(border_line)
    # Affichage du bas du tableau avec la couleur spécifiée
    print('\033[38;5;202m╚' + '═' * (max_width - 2) + '╝\033[0m')


# Définition de la fonction pour filtrer les événements attribués à un utilisateur spécifique
def filtrer_evenements_attribues_a_utilisateur(current_user):
    # Retourner les événements dont le gestionnaire est l'utilisateur courant
    return Evenement.objects.filter(gestionnaire=current_user)
