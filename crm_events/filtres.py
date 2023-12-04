from epic_auth_app.models import Utilisateur
from epic_events_app.models import Evenement
from epic_contracts_app.models import Contrat
from prettytable import PrettyTable
import logging

logger = logging.getLogger(__name__)


def filtrer_utilisateurs_par_departement(departement_code):
    if departement_code != 'AUT':
        return Utilisateur.objects.filter(department=departement_code)
    else:
        return Utilisateur.objects.exclude(department__in=['ADM', 'GES', 'COM', 'SUP'])


def afficher_utilisateurs(utilisateurs):
    table = PrettyTable()
    table.field_names = ["ID", "Email", "Prénom", "Nom", "Département", "Superutilisateur"]
    table.border = False
    table.header = True
    table.align = 'l'

    if utilisateurs.exists():
        for utilisateur in utilisateurs:
            table.add_row([
                " " + str(utilisateur.id) + " ",
                " " + utilisateur.email + " ",
                " " + utilisateur.first_name + " ",
                " " + utilisateur.last_name + " ",
                " " + utilisateur.department + " ",
                " Yes " if utilisateur.is_superuser else " No ",
            ])

        max_width = max(len(str(row)) for row in table.get_string().split("\n")) + 6
        border_line = '\033[94m╠' + '═' * (max_width - 2) + '╣\033[0m'
        light_blue_color_code = '\033[96m'  # Code couleur ANSI pour un bleu clair

        print(light_blue_color_code + '╔' + '═' * (max_width - 2) + '╗\033[0m')
        for i, line in enumerate(table.get_string().split("\n")):
            print(light_blue_color_code + '║' + line.ljust(max_width - 2) + '║\033[0m')
            if i == 0:
                print(light_blue_color_code + border_line + '\033[0m')
        print(light_blue_color_code + '╚' + '═' * (max_width - 2) + '╝\033[0m')
    else:
        print("\033[93mAucun utilisateur disponible.\033[0m")


def filtrer_evenements_sans_support():
    return Evenement.objects.filter(gestionnaire__isnull=True)


def afficher_evenements(evenements):
    table = PrettyTable()
    table.field_names = ["ID", "Nom", "Début", "Fin", "Lieu", "Type", "Statut", "Contrat ID", "Gestionnaire"]
    table.border = False
    table.header = True
    table.align = 'l'

    for evenement in evenements:
        gestionnaire_email = evenement.gestionnaire.email if evenement.gestionnaire else 'N/A'
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
    light_violet_color_code = '\033[95m'  # Code couleur ANSI pour un violet clair
    border_line = light_violet_color_code + '╠' + '═' * (max_width - 2) + '╣\033[0m'

    # Affichage du tableau avec les bordures personnalisées et en violet clair
    print(light_violet_color_code + '╔' + '═' * (max_width - 2) + '╗\033[0m')
    for i, line in enumerate(table.get_string().split("\n")):
        print(light_violet_color_code + '║' + line.ljust(max_width - 2) + '║\033[0m')
        if i == 0:
            print(border_line)
    print(light_violet_color_code + '╚' + '═' * (max_width - 2) + '╝\033[0m')


def filtrer_contrats_non_signes():
    return Contrat.objects.filter(statut='EN_ATTENTE')


def filtrer_contrats_non_entierement_payes():
    return Contrat.objects.filter(montant_restant__gt=0)


def afficher_contrats(contrats):
    logger.info("Affichage des contrats filtrés")

    if not contrats.exists():
        logger.warning("Aucun contrat correspondant aux critères pour l'affichage")
        print("\033[93mAucun contrat correspondant aux critères.\033[0m")
        return

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
