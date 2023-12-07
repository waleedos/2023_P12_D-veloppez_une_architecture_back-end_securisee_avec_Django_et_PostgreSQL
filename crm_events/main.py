import os
import django
import logging
import sentry_sdk

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_events.settings')
django.setup()


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Démarrage de l'application")


sentry_sdk.init(
    dsn="https://06c9f2cd3ff6e7691aa2488eacbbf2b9@o4506331927609344.ingest.sentry.io/4506331936587776",
    traces_sample_rate=1.0
)

# Importations après la configuration de Django
import user_management as um                    # noqa: E402
import client_management as cm                  # noqa: E402
from contract_management import gerer_contrats  # noqa: E402
from event_management import gerer_events       # noqa: E402

# Variable pour garder en mémoire l'utilisateur actuellement connecté
current_authenticated_user = None


def print_menu_header(title, width=50):
    print("\033[93m" + '╔' + '═' * (width - 2) + '╗' + "\033[0m")  # En-tête avec couleur verte
    print("\033[93m║" + title.center(width - 2) + "║\033[0m")
    print("\033[93m" + '╚' + '═' * (width - 2) + '╝' + "\033[0m")


def main_menu():
    global current_authenticated_user

    while True:
        print_menu_header("Bienvenue dans CRM Epic Events", 34)
        print("1. Login")
        print("2. Logout")
        print("3. Gérer les Utilisateurs")
        print("4. Gérer les Clients")
        print("5. Gérer les Contrats")
        print("6. Gérer les Événements")
        print("7. Vérifier la Sécurité")
        print("8. Journalisation et Suivi")
        print("9. Quitter")

        choice = input("\033[34m\nEntrez votre choix: \033[0m")

        if choice == '1':
            current_authenticated_user = um.login(show_token=False)
        elif choice == '2':
            um.logout()
            current_authenticated_user = None
        elif choice == '3':
            um.gerer_utilisateurs(current_authenticated_user)
        elif choice == '4':
            cm.gerer_clients(current_authenticated_user)
        elif choice == '5':
            if not current_authenticated_user:
                print("\033[91mVeuillez vous connecter d'abord.\033\n[0m")
                continue
            gerer_contrats(current_authenticated_user)
        elif choice == '6':
            if not current_authenticated_user:
                print("\033[91mVeuillez vous connecter d'abord.\033[0m")
                continue
            gerer_events(current_authenticated_user)
        elif choice == '9':
            logger.info("L'utilisateur a quitté l'application")
            print("Au revoir !")
            break
        else:
            print("\033\n[91mChoix invalide. Veuillez réessayer.\033\n[0m")


if __name__ == "__main__":
    main_menu()
