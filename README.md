# AlgoArena

AlgoArena est une plateforme en ligne permettant aux développeurs d'entraîner et de tester leurs intelligences artificielles (IA) dans un environnement de jeu compétitif. Son objectif principal est de fournir un cadre pour l'apprentissage par renforcement et l'optimisation des algorithmes d'IA à travers des simulations de jeu opposant différentes IA les unes aux autres.

Les développeurs peuvent soumettre leur code IA à la plateforme, qui organisera alors des matchs contre d'autres IA soumises. Les résultats de ces matchs, y compris les vidéos de simulation, sont enregistrés et utilisés pour calculer les classements Elo des différentes IA. Cette fonctionnalité permet aux développeurs de suivre la progression de leurs IA et de les comparer à d'autres implémentations.

## Structure des répertoires

- `algoarena/` : Contient le projet SvelteKit qui sert de front-end pour la plateforme. C'est l'interface utilisateur permettant aux développeurs de soumettre leur code IA, de consulter les classements et les résultats des matchs.
- `dockerized/` : Contient le code pour la configuration Docker qui exécute toutes les simulations de matchs dans un environnement sécurisé.
- `game/` : Contient la logique de base du jeu avec laquelle les IA interagissent.

## Prérequis

- Docker
- Python 3
- Node.js (v16 ou supérieur)
- Compte et base de données Xata

## Configuration

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

3. Accédez au répertoire `algoarena/` et installez les dépendances du projet :

```bash
cd algoarena
npm install
```

4. Construisez le projet SvelteKit :

```bash
npm run build
```

Cela créera une version optimisée de votre application SvelteKit dans le dossier `build/`.

## Exécution de l'application

1. Construisez l'image Docker :

```bash
docker build -t algoarena .
```

2. Exécutez le conteneur Docker :

```bash
docker run -it algoarena
```

Cela lancera le processus de simulation de match, qui suit les étapes suivantes :

1. Récupérer les informations des utilisateurs depuis la base de données Xata.
2. Sélectionner aléatoirement deux utilisateurs pour la simulation de match.
3. Vérifier si un match entre les utilisateurs sélectionnés existe déjà dans la base de données.
4. Si aucun match existant n'est trouvé, créer un nouvel enregistrement de match.
5. Récupérer le code IA des utilisateurs sélectionnés depuis la base de données.
6. Écrire le code IA dans les fichiers `player1.py` et `player2.py`.
7. Exécuter la simulation de match dans un environnement sécurisé à l'aide de Docker, empêchant tout accès accidentel au réseau.
8. Mettre à jour les classements Elo des utilisateurs en fonction du résultat du match.
9. Stocker le résultat du match et la vidéo dans la base de données Xata.

3. Pour prévisualiser le front-end SvelteKit localement, accédez au répertoire `algoarena/` et exécutez :

```bash
npm run preview
```

Cela démarrera un serveur de développement local, et vous pourrez accéder au front-end à l'adresse `http://localhost:3000`.

## Déploiement

Pour déployer le front-end SvelteKit sur un service d'hébergement comme Vercel, vous pouvez simplement télécharger le contenu du dossier `algoarena/build/`.

## Intelligence Artificielle du Jeu

L'intelligence artificielle du jeu est implémentée dans les fichiers `player1.py` et `player2.py`. Ces fichiers sont automatiquement mis à jour avec le code IA récupéré depuis la base de données Xata avant chaque simulation de match. Vous pouvez modifier et mettre à jour le code IA dans la base de données Xata, et les changements seront répercutés dans les simulations de match.

## Base de données Xata

La base de données Xata est utilisée pour stocker les données suivantes :

- **Utilisateurs** : Stocke les informations des utilisateurs, y compris l'e-mail, le nom, le classement Elo et le code IA.
- **Matchs** : Stocke les détails des matchs, y compris les utilisateurs participants, le gagnant et la vidéo du match.