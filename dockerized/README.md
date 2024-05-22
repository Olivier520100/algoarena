
**# AlgoArena**  

AlgoArena est une plateforme permettant d'exécuter des simulations de jeux entre des joueurs IA et de suivre leurs classements Elo. Elle utilise une base de données Xata pour stocker les informations des utilisateurs, les détails des matchs et le code IA. Les simulations de jeu sont exécutées dans un environnement sécurisé à l'aide de conteneurs Docker pour empêcher tout accès accidentel au réseau.

**## Prérequis**

- Docker
- Python 3 
- Compte et base de données Xata

**## Configuration**

1. Installez les packages Python requis :

```bash
pip install -r requirements.txt
```

2. Créez un fichier `.env` à la racine du projet avec les variables d'environnement suivantes :

```
XATA_DATABASE_URL=<votre_url_base_de_données_xata>
XATA_API_KEY=<votre_clé_api_xata>
```

Remplacez `<votre_url_base_de_données_xata>` et `<votre_clé_api_xata>` par l'URL de votre base de données Xata et votre clé API.

**## Utilisation**

1. Construisez l'image Docker :

```bash
docker build -t algoarena .
```

2. Exécutez le conteneur Docker :

```bash
docker run -it algoarena
```

Cela démarrera le processus de simulation de jeu, qui suit les étapes suivantes :

1. Récupérer les informations des utilisateurs depuis la base de données Xata.
2. Sélectionner deux utilisateurs aléatoires pour la simulation de jeu.
3. Vérifier si un match entre les utilisateurs sélectionnés existe déjà dans la base de données.
4. Si aucun match existant n'est trouvé, créer un nouvel enregistrement de match.
5. Récupérer le code IA des utilisateurs sélectionnés depuis la base de données.
6. Écrire le code IA dans les fichiers `player1.py` et `player2.py`.
7. Exécuter la simulation de jeu dans un environnement sécurisé à l'aide de Docker, empêchant tout accès accidentel au réseau.
8. Mettre à jour les classements Elo des utilisateurs en fonction du résultat du jeu.
9. Stocker le résultat du jeu et la vidéo dans la base de données Xata.

**## IA de jeu**

L'IA de jeu est implémentée dans les fichiers `player1.py` et `player2.py`. Ces fichiers sont automatiquement mis à jour avec le code IA récupéré depuis la base de données Xata avant chaque simulation de jeu.

Vous pouvez modifier et mettre à jour le code IA dans la base de données Xata, et les changements seront répercutés dans les simulations de jeu.

**## Base de données Xata**

La base de données Xata est utilisée pour stocker les données suivantes :

- **Utilisateurs** : Stocke les informations des utilisateurs, y compris l'e-mail, le nom, le classement Elo et le code IA.
- **Matchs** : Stocke les détails des matchs, y compris les utilisateurs participants, le gagnant et la vidéo du jeu.

