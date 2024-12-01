# ZeBot

ZeBot est un bot discord qui mets à disposition du serveur Mipsology plusieurs applications :
FoodDemocraty : qui permet d'organiser des votes au jugement majoritaire pour choisir un ou plusieurs restaurants.

## Bien démarrer

### Utilisateur


### Developpeur

## Déploiement

Le projet peut être déployé de deux façons différentes :
- en local : plus de fléxibilité et rapiditié de debug
- avec docker : plus simple, plus automatique et environnement maitrisé

### Déploiment en local

#### Mettre en place l'environnement python
```
python -m venv .env               # Create a virtual environnement / /!\ Don't commit the .env directory
source .env/bin/activate          # Apply virtual env / Do this each time, you reopen a terminal
pip install -r requirements.txt   # Install all required librairies in the virtual env
```

#### Installer postgresql (la base de données)
```
sudo apt install postgresql postgresql-contrib
```

#### Créer un utilisateur de la DB correspondant à l'utilisateur admin du serveur
```
sudo -iu postgres psql
CREATE USER ${USER};
ALTER USER ${USER} PASSWORD '<PWD>' SUPERUSER CREATEDB CREATEROLE LOGIN;
```

#### Créer le fichier de configuration de Django
Avant de lancer le serveur, il faut créer un fichier **django.conf** dans le dossier **backend** de la forme suivante :  
```
secret_key                  = 'cette cle est fausse'
debug_en                    = true
allowed_host_list           = []
csrf_trusted_origin_list    = []
db_name                     = "mbbv_db"
db_password                 = "0000"
db_host                     = "localhost"
db_port                     = 5432
site_base_url               = "http://localhost:8000"
```

Une __secret_key__ peut être générée en utilisant `python manage.py shell` :  
```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### Initialiser la base de données et démarrer les services
```
sudo ./deploy.sh 0 1 0 0 0
```

#### Créer le fichier de configuration DiscordBot
Avant de démarrer le serveur, il faut créer un fichier **discord.conf** dans le dossier **DiscordBot** de la forme suivante :  
```
discord_token               = "ce token est faux"
admin_channel_id            = 0
```

#### Créer les fichiers de configuration des modules de DiscordBot
**FoodDemocracy :**
```
channel_id      = 1305493938425167903
role_id         = 1312724232945270885
api_base_url    = "http://127.0.0.1:8000/FoodDemocracy"
emoji_list      = ["\U0001F92E", "\U0001F922", "\U0001F610", "\U0001F924", "\U0001F60D"]
```

#### Execution

A chaque démarrage de la machine, dans le dossier **backend** :
```
sudo ./deploy.sh 0 0 0 0 0
```

Pour lancer le serveur, dans le dossier **backend** :
```
python manage.py runserver
```

### Deploiment avec Docker

#### Modifier le fichier de configuration de Django
Les valeurs suivantes du fichier **docker/backend/django.conf** doivent être actualisées :
- secret_key : voir plus haut
- allowed_host_list : liste des adresses IPs sur lequel le serveur va être joignable
- db_password

#### Modifier le fichier de configuration de DiscordBot
Les valeurs suivantes du fichier **docker/discord/discord.conf** doivent être actualisées :
- discord_token : récupérer le token sur le portail developpeur de Discord
- *_channel_id : récupérer les ids des channels sur le serveur Discord cible
- *_role_id : récupérer les ids des rôles sur le serveur Discord cible

#### Execution
Créer l'image docker (à relancer à chaque modification des sources) :
```
docker compose build
```

Lancer le docker :
```
docker compose up
```
