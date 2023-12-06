<h1 align="center">OC Project N°12 - Epic_Events CRM's</h1>
<h2 align="center">P12 Développez une architecture back-end sécurisée avec Python et SQL</h1>

![Logo LITReview](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/photo/entete.png)

## Compétences aquises et évaluées de ce projet : 
* Mettre en œuvre une base de données sécurisée avec Python et SQL

## Technologies Utilisées

- **Langage Principal** : Python (Version 3.11.7)
- **Framework Web** : Django 5.0
- **Base de Données** : PostgreSQL 14.9 (via psycopg2)
- **Sécurité** : Bcrypt pour le hachage des mots de passe
- **Gestion de Configuration** : Django-environ, python-decouple, python-dotenv
- **Monitoring** : Sentry SDK pour le suivi des erreurs
- **Tests et Assurance Qualité** : Pytest avec pytest-django, Flake8 pour l'analyse de code
- **CLI et Rapports** : Jinja2 pour les templates, PrettyTable pour les affichages tabulaires
- **Dépendances Diverses** : Certifi, urllib3, MarkupSafe, etc.



## Introduction :
Epic_Events CRM's est un système CRM (Customer Relationship Management) sécurisé interne à l'entreprise, élaboré pour collecter et traiter les données des clients et de leurs événements. La société Epic Events est une entreprise de conseil et de gestion dans l'événementiel qui répond aux besoins des start-up voulant organiser des « fêtes épiques » .

## Auteurs
L'équipe est composée de EL-WALID EL-KHABOU et de son mentor OpenClassRooms.

## Licence
Logiciel gratuit.

## Mission
Après avoir organisé des centaines d’évènements, Epic Events a plusieurs dizaines de clients réguliers. Malheureusement, tout le travail se base sur des outils inadaptés et une solution de CRM qui fait cruellement défaut pour toutes les équipes et les départements de la société.

Nous avons décidé d'adopter une approche proactive pour remédier à la situation, en élaborant un système CRM sécurisé interne à l'entreprise, qui nous aiderait à collecter et à traiter les données des clients et de leurs événements. Cela devrait rassurer nos clients et, espérons-le, leur redonner confiance en nous en leur montrant que nous prenons les choses au sérieux.

L'équipe a dressé une liste de document pour cette mission : 

- **La Mission** : [La Mission](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/Mission/1.Mission.pdf).
- **Le cahier des charges** : [Le cahier des charges](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/Mission/2.Cahier-des-charges.pdf).
- **Le guide d'étapes clés** : [Le guide d'étapes clés pour l'avancement du projet](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/Mission/3.Guide-%C3%A9tapes-cl%C3%A9s.pdf) 

### Voici La stucture actuelle et finale de ce projet :

- **La structure du projet** : [La structure du projet](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/structure_de_ce_projet.txt).


### Comment cloner ce référentiel GitHub: 

Vous pouvez cloner et forker le repo en totalité via HTTPS:
``` 
git clone https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL.git
```

Vous pouvez aussi cloner et forker le repo en totalité via SSH:
``` 
git clone git@github.com:waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL.git
```

Ou encore, vous pouvez télécharger le dossier entier compressé (.zip) :
- [Téléchargez le dossier complet de ce projet](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/archive/refs/heads/main.zip).

### Accédez à la racine du projet:
```
cd [Nom de votre dossier décompressé ou cloné]
```

### Vérification si vous etes au bon dossier : 
```
ls
```
La sortie de cette commande devra vous afficher les dossiers et fichiers suivant : 
- crm_events (dossier) 
- docs (dossier) 
- README.md (fichier) 
- requirements.txt (fichier) 
- structure_de_ce_projet.txt (fichier)

### Créer un environnement virtuel Python (sur une machine linux):
```
python -m venv venv
```

### Activer l'environnement virtuel Python:
```
source env/bin/activate # Sur Linux/Mac
env\Scripts\activate # Sur Windows
```

### Importez et installez tous les modules:
```
pip install -r requirements.txt
```

### Créer un Fichier .env à la racine du projet (dans le dossier crm_events): 
```
mkdir .env
```

### Générer une nouvelle clé secrète, vous pouvez utiliser la console Python:
- Démarrez la console python 
```
python
# ou
python3
```
- Copier/coller le code suivant et validez :
```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
Vous allez voir que python a généréré une SECRET_KEY du style :
```
j^$-6tjo-s45j(6)-_=fmb%p4+2enehxlmsuzy8szmozlhc5^6
```

### Générer une nouvelle JWT_SECRET_KEY toujours avec la console Python:
- Copier/coller le code suivant et validez :
```
import os
print(os.urandom(24).hex())
```
Vous allez voir que python a généréré une JWT_SECRET_KEY du style :
```
daae87ae289ac5f6b89a0ffb0a82ee99cc1a1af95b0669e2
```
### Remplissez le fichier .env créé avec les informations créés suivantes (à titre d'exemple):
```
SECRET_KEY="votre clé que python viens de générer"
JWT_SECRET_KEY=daae87ae289ac5f6b89a0ffb0a82ee99cc1a1af95b0669e2
DEBUG=True
DB_NAME=crm_events
DB_USER=Non_utilisateur_de_la_base_de_donnée_postgres (par exemple = postgre)
DB_PASSWORD="un_password_de_votre_choix"
DB_HOST=localhost
DB_PORT=5432
```
et enregistrer le fichier

### Création d'un SuperUtilisateur:
```
# assurez vous que vous êtes toujours dans le dossier /crm_events, sinon 
cd crm_events

# puis
python manage.py createsuperuser
```
Lorsque vous exécutez cette commande, Django vous demandera de fournir un nom d'utilisateur, une adresse e-mail et un mot de passe pour le nouveau SuperUtilisateur. Suivez les instructions à l'écran pour compléter la création de ce compte. Suivez les étapes dans la console en entrant par-exemple : 

- e-mail : admin@admin.com
- Prénom : admin
- Nom : admin
- Passwor: votre mots de pass

Ce SuperUtilisateur aura accès à l'interface d'administration de Django et pourra gérer l'ensemble du site, ce qui inclut la capacité de créer, modifier et supprimer des utilisateurs, ainsi que d'effectuer d'autres tâches administratives.

## Configuration de la Base de Données PostgreSQL
Installer PostgreSQL :

Assurez-vous d'avoir PostgreSQL installé sur votre système. Si ce n'est pas le cas, vous pouvez le télécharger depuis le site officiel de PostgreSQL et l'installer.

### Création de la Base de Données :

Ouvrez un terminal et connectez-vous à votre instance PostgreSQL avec l'utilisateur approprié (généralement "postgres") et il doit être le même que vous avez insérer dans le fichier .env:
```
sudo -u postgres psql
```

### Créez la base maintenant :
une nouvelle base de données avec le nom spécifié dans votre fichier .env (par exemple, crm_events) :
```
CREATE DATABASE crm_events;
```
Si vous avez un message vous disant que cette base de donnée existe deja, cela veut dire que DJANGO a déja fait le boulot pour vous.

Vous pouvez vérifier l’existence des données dans la base de donnée, par exemple via l'interface graphique de Django (Admin), si vous ne trouvez pas les données déjà existants, restaurer la Base de Données à partir du Backup :

### Restaurer la Base de Données à partir du Backup :

Utilisez la sauvegarde ma_bdd_backup.sql disponible dans le dépôt GitHub pour restaurer les données dans la base de données nouvellement créée :
```
psql -U votre_nom_utilisateur_postgres -d crm_events -a -f ma_bdd_backup.sql
```

### Revérifiez bien les Variables d'Environnement :

Assurez-vous que les informations de connexion à la base de données dans le fichier .env correspondent à la base de données PostgreSQL que vous venez de créer :
DB_NAME : Le nom de la base de données doit correspondre à celui que vous avez créé.
DB_USER : Le nom d'utilisateur PostgreSQL que vous avez utilisé pour la restauration de la sauvegarde.
DB_PASSWORD : Le mot de passe de l'utilisateur PostgreSQL.

### Exécuter les Migrations Django :

Une fois que la base de données est configurée et restaurée, vous pouvez exécuter les migrations Django pour créer les tables nécessaires dans la base de données :
```
python manage.py makemigrations
# puis
python manage.py migrate
```

## Avertissement de Sécurité : 
Les informations contenues dans le tableau suivant sont présentées uniquement à des fins de démonstration et de test. Dans un environnement de production réel, il est fortement déconseillé de stocker ou de partager des informations sensibles de cette manière, en raison des risques évidents de sécurité et de confidentialité. Ce tableau est mis en ligne dans ce format spécifique pour faciliter la tâche des utilisateurs souhaitant tester et évaluer ce projet. Veuillez vous assurer de traiter toutes les données sensibles avec les précautions de sécurité adéquates dans vos applications.

| Département |             Utilisateur            |  Password  |  Prénom  |     Nom     |
|:-----------:|:----------------------------------:|:----------:|:--------:|:-----------:|
|     ADM     |    adm2@epic-events.com            |  Base1234  |   Adam   |    SMITH    |
|     ADM     |    adm3@epic-events.com            |  Base9876  |  Pamela  |  ANDERSON   |
|             |                                    |            |          |             |
|     GES     |    ges1@epic-events.com            | Bigar1234  |  Romin   |   LEFEBRE   |
|     GES     |    ges2@epic-events.com            | Bagar9876  |  Amelie  |    DUPON    |
|     GES     |    ges3@epic-events.com            |  Base1234  |  Bruno   |   RUDFORD   |
|     GES     |    ges4@epic-events.com            |  Base9876  |  Nancie  |   COUREL    |
|             |                                    |            |          |             |
|     COM     |    com1@epic-events.com            | Arizon1234 |  Julien  |    ABRON    |
|     COM     |    com2@epic-events.com            | AriZon9876 | Lucette  |  GHORBAL    |
|     COM     |    com3@epic-events.com            | Arnold8877 |   Jean   |   BERNARD   |
|     COM     |    com4@epic-events.com            | Ardise6565 |   Katia  |  KAMOVICH   |
|     COM     |    com5@epic-events.com            |  Base2345  |  Abdel   |   FOURATI   |
|             |                                    |            |          |             |
|     SUP     |    sup1@epic-events.com            | Crypto8787 |  Ahmed   |   KHALIF    |
|     SUP     |    sup2@epic-events.com            | Crypto9898 |  Simone  |   RENARD    |
|     SUP     |    sup3@epic-events.com            | Crypos0123 |  Velery  |    JUDON    |
|     SUP     |    sup4@epic-events.com            | Crypos5678 |  Malik   |   CHANTAL   |
|             |                                    |            |          |             |
|     TST     |    tst1@epic-events.com            |  Tests1234 |   Test   |   LETEST    |


### Démarrage du serveur :
```
# assurez vous que vous etes toujours dans le dossier /crm_events, sinon 
cd crm_events

# puis
python manage.py runserver
```

### Il est temps maintenant de démarrer l'application sur votre navigateur :
Ouvrez votre navigateur et naviguez vers une des deux adresse suivantes :
```
http://127.0.0.1:8000/admin

# ou bien

http://localhost:8000/admin
```

### Connectez vous en tant que SuperUtilisateur : 
Remplissez les identifiants (E-mail et Password) avec les quels vous avez créé votre SuperUtilisateur, et validez.

![Vous verrez l'ecran suivant](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/photo/log_in_admin.png)

## Démarrez le CLI : 

Dans le dossier principale du projet : /crm_events, démarrez le projet avec la commande suivante : 
```
python main.py
```

### Les 5 Menus principaux de l'application :

Quand vous démarrez l'application CRM en CLI, c'est à dire en ligne de commande, voici le 5 menus principaux de cette dernière : 

![Les Menus Principaux](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/photo/crm-cli.png)


## Les tests : :


## Les "blogger" en "live" :

## La journalisation totale avec "Sentry" :

## Vérification & Contrôle du code avec flake8 :
```
flake8 --format=html --htmldir=flake-report
```


## Powered by EL-WALID EL-KHABOU
```
E-mail : ewek.dev@gmail.com
```
