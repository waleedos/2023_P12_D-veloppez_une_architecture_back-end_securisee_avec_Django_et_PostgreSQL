<h1 align="center">OC Project N°12  -  Epic_Events CRM's</h1>
<h2 align="center">P12 Développez une architecture back-end sécurisée avec Python et SQL</h1>

![Logo LITReview](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/photo/entete.png)


## Compétences aquises et évaluées de ce projet : 
* Mettre en œuvre une base de données sécurisée avec Python et SQL


## Technologies Utilisées

- **Langage Principal**          : Python (Version 3.10.12)
- **Framework Web**              : Django 4.2.7
- **Base de Données**            : PostgreSQL 14.9 (via psycopg2)
- **Sécurité**                   : Bcrypt pour le hachage des mots de passe
- **Gestion de Configuration**   : Django-environ, python-decouple, python-dotenv
- **Monitoring**                 : Sentry SDK pour le suivi des erreurs
- **Tests et Assurance Qualité** : Pytest avec pytest-django, Flake8 pour l'analyse de code
- **CLI et Rapports**            : Jinja2 pour les templates, PrettyTable pour les affichages tabulaires
- **Dépendances Diverses**       : Certifi, urllib3, MarkupSafe, etc.




## Introduction :
Epic_Events CRM's est un système CRM (Customer Relationship Management) sécurisé interne à l'entreprise, élaboré pour collecter et traiter les données des clients et de leurs événements.  La société Epic Events est une entreprise de conseil et de gestion dans l'événementiel qui répond aux besoins des start-up voulant organiser des « fêtes épiques » .

## Auteurs
L'équipe est composée de EL-WALID EL-KHABOU et de son mentor OpenClassRooms.

## Licence
Logiciel gratuit.

## Mission
Après avoir organisé des centaines d’évènements, Epic Events a plusieurs dizaines de clients réguliers. Malheureusement, tout le travail se base sur des outils inadaptés et une solution de CRM qui fait cruellement défaut pour toutes les équipes et les départements de la société.

Nous avons décidé d'adopter une approche proactive pour remédier à la situation, en élaborant un système CRM sécurisé interne à l'entreprise, qui nous aiderait à collecter et à traiter les données des clients et de leurs événements. Cela devrait rassurer nos clients et, espérons-le, leur redonner confiance en nous en leur montrant que nous prenons les choses au sérieux.

L'équipe a dressé une liste de document pour cette mission : 

- **La Mission**                : [La Mission](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/Mission/1.Mission.pdf).
- **Le cahier des charges**     : [Le cahier des charges](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/Mission/2.Cahier-des-charges.pdf).
- **Le guide d'étapes clés**    : [Le guide d'étapes clés pour l'avancement du projet](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/Mission/3.Guide-%C3%A9tapes-cl%C3%A9s.pdf) 


### Voici La stucture actuelle et finale de ce projet :

- **La stucture du projet**    : [La stucture du projet](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/structure_de_ce_projet.txt).



### La base de données : 




### Comment cloner ce référentiel GitHub: 

Vous pouvez cloner et forker le repo en totalité via HTTPS:
``` 
git clone https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL.git
```

Vous pouvez aussiz cloner et forker le repo en totalité via SSH:
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
source env/bin/activate  # Sur Linux/Mac
env\Scripts\activate  # Sur Windows
```

### Importez et installez tous les modules:
```
pip install -r requirements.txt
```

### Création d'un SuperUtilisateur:
```
# assurez vous que vous etes toujours dans le dossier /crm_events, sinon 
cd crm_events

# puis
python manage.py createsuperuser
```

Lorsque vous exécutez cette commande, Django vous demandera de fournir un nom d'utilisateur, une adresse e-mail et un mot de passe pour le nouveau SuperUtilisateur. Suivez les instructions à l'écran pour compléter la création de ce compte.

Ce SuperUtilisateur aura accès à l'interface d'administration de Django et pourra gérer l'ensemble du site, ce qui inclut la capacité de créer, modifier et supprimer des utilisateurs, ainsi que d'effectuer d'autres tâches administratives.

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

#### Connectez vous en tant que SuperUtilisateur : 
Remplissez les identifiants (E-mail et Password) avec les quels vous avez créé votre SuperUtilisateur, et validez.

![Vous verrez l'ecran suivant](https://github.com/waleedos/2023_P12_D-veloppez_une_architecture_back-end_securisee_avec_Django_et_PostgreSQL/blob/main/docs/photo/log_in_admin.png)



# Les tests : 
Dans ce projet, plus de 58 tests en tout et pour tout ont été élaborés comme suit : 

| Nature des tests            | Nombre                       | Commande globale                                         |
|-----------------------------|------------------------------|----------------------------------------------------------|
| 1. Les tests unitaires      | 36 tests                     | ```pytest tests/unit/```                                 |
| 2. Les tests d'intégration  | 10 tests                     | ```pytest tests/integrity/```                            |
| 3. Les tests fonctionnels   | 12 tests                     | ```pytest tests/fonctionnels/```                         |
| 4. Les tests de performance | 1 test global                |1 test global donnant 2 rapports complets grâce à LOCUST  |


## Les tests unitaires : 36 tests, vous pouvez les executez en une seule fois par la commande suivante :
```
pytest tests/unit/
```
![Execution de tous les tests unitaires à la fois](https://github.com/waleedos/2023_P11_Ameliorer-app-Web_Python-par-des-tests-et-du-d-bogage_GUDLFT/blob/QA/docs/photos/unit.png)


## Les tests d'intégration ou integrity-tests : 10 tests, vous pouvez les executez en une seule fois par la commande suivante :
```
pytest tests/integrity/
```
![Execution de tous les tests fonctionnels à la fois](https://github.com/waleedos/2023_P11_Ameliorer-app-Web_Python-par-des-tests-et-du-d-bogage_GUDLFT/blob/QA/docs/photos/integrity.png)


## Les tests fonctionnels : 12 tests, vous pouvez les executez en une seule fois par la commande suivante :
```
pytest tests/fonctionnels/
```
![Execution de tous les tests fonctionnels à la fois](https://github.com/waleedos/2023_P11_Ameliorer-app-Web_Python-par-des-tests-et-du-d-bogage_GUDLFT/blob/QA/docs/photos/fonctionnels.png)


## Les tests de performance : 1 test global donnant deux rapports complets grace à LOCUST.

### Installation de locust : 
Installez locust en copiant/collant la commande suivante :
```
pip install locust
```

### Execution du test LOCUST : 
Rendez vous dans le dossier qui habite le fichier locustfile.py avec la commande suivante : 
```
cd tests/performance
```

### Démarrez le test LOCUST: 
ATTENTION,  il est impératif que votre application soit fonctionnelle et le serveur flask soit démarré
avant d'executer le test LOCUST.

Executez le test locust avec la commande suivante :
```
locust
```
Puis ouvrez une autre fenetre de votre navigateur, et mettez vous sur l'adresse suivante : 
```
http://127.0.0.1:8089
```

### Lancez LOCUST :
Une fois que vous vous rendez sur l'adresse mentionnée dans la commande précédente, vous serez sur une page comme la suivante:

![LOCUST](https://github.com/waleedos/2023_P11_Ameliorer-app-Web_Python-par-des-tests-et-du-d-bogage_GUDLFT/blob/QA/docs/photos/locust.png)

Remplissez ces 3 cases comme mentionné dans cette photo et validez en clickant sur 'Start swarming'


### Execution d'un seul test à la fois : 

Si vous voulez executer un seul test à la fois, vous pouvez utiliser la commande suivante : 
```
pytest tests/dossier/nom_du_test
```

Par exemple, si vous voulez executer le test unitaire nommé 'test_home_page_load.py' existant dans le dossier de tests 'unit'
vous devriez l'executer avec la commande suivante : 
```
pytest tests/unit/test_home_page_load.py
```

## Test & Rapports de couverture : 
```
pytest --cov=. --cov-report term-missing --cov-report html
```


### Vérification & Contrôle du code avec flake8 :
```
flake8 --format=html --htmldir=flake-report
```


# les rapports de cette mission & projet : 

1. [Rapports d'execution de tous les tests](https://github.com/waleedos/2023_P11_Ameliorer-app-Web_Python-par-des-tests-et-du-d-bogage_GUDLFT/blob/QA/docs/rapport/tous-les-tests.pdf).

2. [Rapports d'execution de locust pour 6 utilisateurs et spawn-rate = 1](https://github.com/waleedos/2023_P11_Ameliorer-app-Web_Python-par-des-tests-et-du-d-bogage_GUDLFT/blob/QA/docs/rapport/locust-6-1.pdf).

3. [Rapports d'execution de locust pour 6 utilisateurs et spawn-rate = 6](https://github.com/waleedos/2023_P11_Ameliorer-app-Web_Python-par-des-tests-et-du-d-bogage_GUDLFT/blob/QA/docs/rapport/locust-6-6.pdf).

4. [Rapports de couverture globale](https://github.com/waleedos/2023_P11_Ameliorer-app-Web_Python-par-des-tests-et-du-d-bogage_GUDLFT/blob/QA/docs/rapport/rapport_de_couverture.pdf).

5. [Rapports de couverture pour server.py](https://github.com/waleedos/2023_P11_Ameliorer-app-Web_Python-par-des-tests-et-du-d-bogage_GUDLFT/blob/QA/docs/rapport/rapport_coverage_for_server_py.pdf).

6. [Rapport Flake8](https://github.com/waleedos/2023_P11_Ameliorer-app-Web_Python-par-des-tests-et-du-d-bogage_GUDLFT/blob/QA/docs/rapport/flake8-violations.pdf)


## Powered by EL-WALID EL-KHABOU
```
E-mail : ewek.dev@gmail.com
```