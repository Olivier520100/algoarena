
# AlgoArena

Ce dossier contient une simulation de jeu de stratégie en temps réel (RTS) avec des joueurs IA. Le jeu implique deux équipes qui s'affrontent sur une carte avec différents types de terrain, de ressources et d'unités.

## Aperçu du jeu

Le jeu se déroule sur une carte 2D avec divers types de terrain (eau, sable, herbe, pierre, ponts). Chaque équipe commence avec un château et quelques ressources initiales (bois et pierre). Les joueurs peuvent invoquer différents types d'unités (ouvriers, mêlée, chars, archers, canons de verre) et de bâtiments (châteaux) en utilisant des ressources. Les unités ont différents attributs comme la santé, les dégâts, la vitesse et la portée. L'objectif est de détruire le château de l'adversaire tout en défendant le sien.

## Structure du code

Le code est écrit en Python et utilise les bibliothèques NumPy, Pandas et OpenCV pour la manipulation de données, le traitement d'images et la génération de vidéos.

- `videogeneration.py` : Contient des fonctions pour générer des sprites, rendre la carte du jeu et créer une vidéo à partir des images du jeu.
- `gamebasemain.py` : Implémente la logique principale du jeu, y compris la génération de la carte, le mouvement des unités, les combats, la collecte de ressources et la boucle de jeu.
- `gameRequests.py` : Définit la classe Request pour gérer les actions des joueurs.
- `player.py` : Représente l'état d'un joueur, y compris les unités, les bâtiments, les ressources et les informations sur l'ennemi.
- `run.py` : Point d'entrée pour exécuter la simulation de jeu.

De plus, il y a des fichiers séparés pour les joueurs IA (`player1.py` et `player2.py`) où vous pouvez implémenter vos stratégies d'IA.

## Utilisation

1. Installez les bibliothèques requises (NumPy, Pandas, OpenCV) en utilisant `pip install -r requirements.txt`.
2. Exécutez `run.py` pour démarrer la simulation de jeu.
3. Le jeu générera un fichier vidéo (`videos/gameID1_gameID2.mp4`) montrant la simulation.

## Implémentation de l'IA

Dans AlgoArena, les joueurs peuvent implémenter leurs stratégies d'IA en modifiant la fonction `playerAction` dans les fichiers `player1.py` et `player2.py`. La fonction `playerAction` prend un objet `Player` en entrée et doit renvoyer un objet `Request` avec l'action souhaitée.

## Objet Player

L'objet `Player` contient des informations sur vos unités, bâtiments, ressources et l'état du jeu. Il a les propriétés suivantes :

- `myUnits` : Une liste de dictionnaires représentant vos unités sur la carte. Chaque dictionnaire a les clés suivantes :
  - `type` : Le type d'unité (par exemple, "Worker", "Melee", "Archer", "Tank", "GlassCannon").
  - `health` : La santé actuelle de l'unité.
  - `coordinates` : Une liste contenant les coordonnées x et y de l'unité sur la carte (par exemple, `[5, 10]`).
  - `goal` : Peut être soit un dictionnaire représentant la cible de l'unité (pour attaquer ou collecter des ressources), soit une liste de coordonnées pour le mouvement.

  Exemple d'entrée `myUnits` :
  ```python
  {
    "type": "Melee",
    "health": 20,
    "coordinates": [3, 7],
    "goal": {
      "type": "Worker",
      "health": 15,
      "coordinates": [5, 9]
    }
  }
  ```

- `myBuildings` : Une liste de dictionnaires représentant vos bâtiments sur la carte. Chaque dictionnaire a les clés suivantes :
  - `type` : Le type de bâtiment (par exemple, "Castle").
  - `health` : La santé actuelle du bâtiment.
  - `coordinates` : Une liste contenant les coordonnées x et y du bâtiment sur la carte.

  Exemple d'entrée `myBuildings` :
  ```python
  {
    "type": "Castle",
    "health": 100,
    "coordinates": [0, 0]
  }
  ```

- `trees` : Une liste de dictionnaires représentant les arbres (ressources) sur la carte. Chaque dictionnaire a les clés suivantes :
  - `type` : Le type de ressource (par exemple, "Tree").
  - `health` : La santé actuelle de la ressource (détermine combien peut être collecté).
  - `coordinates` : Une liste contenant les coordonnées x et y de la ressource sur la carte.

  Exemple d'entrée `trees` :
  ```python
  {
    "type": "Tree",
    "health": 10,
    "coordinates": [8, 12]
  }
  ```

- `enemyUnits` : Une liste de dictionnaires représentant les unités ennemies sur la carte. La structure est la même que `myUnits`.
- `enemyBuildings` : Une liste de dictionnaires représentant les bâtiments ennemis sur la carte. La structure est la même que `myBuildings`.
- `wood` : La quantité de ressources en bois que vous avez actuellement.
- `stone` : La quantité de ressources en pierre que vous avez actuellement.
- `summoncoords` : Une liste de listes de coordonnées où vous pouvez invoquer de nouvelles unités (par exemple, `[[5, 8], [7, 10], ...]`).

## Objet Request

L'objet `Request` est utilisé pour spécifier l'action que vous voulez effectuer dans le jeu. Il a deux propriétés :

- `gameObjectDict` : Un dictionnaire représentant l'objet de jeu (unité ou bâtiment) avec lequel vous voulez agir. Ce dictionnaire doit correspondre à l'un des dictionnaires dans `myUnits` ou `myBuildings`.

  Exemple de `gameObjectDict` :
  ```python
  {
    "type": "Worker",
    "health": 15,
    "coordinates": [2, 5],
    "goal": None
  }
  ```

- `gameRequestDict` : Un dictionnaire représentant la requête que vous voulez faire pour l'objet de jeu. Ce dictionnaire peut avoir différentes structures selon le type de requête :

  - Requête de mouvement :
    ```python
    {
      "coordinates": [7, 12]
    }
    ```
    Cette requête déplacera l'unité ou le bâtiment spécifié vers les coordonnées données.

  - Requête d'attaque :
    ```python
    {
      "type": "Melee",
      "health": 18,
      "coordinates": [6, 9]
    }
    ```
    Cette requête fera que l'unité ou le bâtiment spécifié attaquera l'unité ou le bâtiment ennemi aux coordonnées données.

  - Requête de collecte de ressources :
    ```python
    {
      "type": "Tree",
      "health": 8,
      "coordinates": [10, 3]
    }
    ```
    Cette requête fera que l'unité spécifiée collectera des ressources de l'arbre aux coordonnées données.
-   Requête d'invocation d'unité :
    ```python
    {
      "coordinates": [4, 6], 
      "type": "Archer"
    }
    ```
    Cette requête invoquera une nouvelle unité Archer aux coordonnées spécifiées (si vous avez suffisamment de ressources).

En combinant `gameObjectDict` et `gameRequestDict`, vous pouvez spécifier diverses actions pour vos unités et bâtiments, comme se déplacer, attaquer, collecter des ressources ou invoquer de nouvelles unités.