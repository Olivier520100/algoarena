# AlgoArena

This folder contains a real-time strategy (RTS) game simulation with AI players. The game involves two teams battling against each other on a map with different terrain types, resources, and units.

## Game Overview

The game is played on a 2D map with various terrain types (water, sand, grass, stone, bridges). Each team starts with a castle and some initial resources (wood and stone). Players can summon different types of units (workers, melee, tanks, archers, glass cannons) and buildings (castles) using resources. Units have different attributes like health, damage, speed, and range. The objective is to destroy the opponent's castle while defending your own.

## Code Structure

The code is written in Python and uses NumPy, Pandas, and OpenCV libraries for data manipulation, image processing, and video generation.

- `videogeneration.py`: Contains functions for generating sprites, rendering the game map, and creating a video from the game frames.
- `gamebasemain.py`: Implements the main game logic, including map generation, unit movement, combat, resource gathering, and game loop.
- `gameRequests.py`: Defines the request class for handling player actions.
- `player.py`: Represents a player's state, including units, buildings, resources, and enemy information.
- `run.py`: Entry point for running the game simulation.

Additionally, there are separate files for the AI players (`player1.py` and `player2.py`) where you can implement your AI strategies.

## Usage

1. Install the required libraries (NumPy, Pandas, OpenCV) using `pip install -r requirements.txt`.
2. Run `run.py` to start the game simulation.
3. The game will generate a video file (`videos/gameID1_gameID2.mp4`) showing the simulation.

## AI Implementation

In AlgoArena, players can implement their AI strategies by modifying the `playerAction` function in the `player1.py` and `player2.py` files. The `playerAction` function takes a `Player` object as input and should return a `Request` object with the desired action.

## Player Object

The `Player` object contains information about your units, buildings, resources, and the game state. It has the following properties:

- `myUnits`: A list of dictionaries representing your units on the map. Each dictionary has the following keys:
  - `type`: The type of unit (e.g., "Worker", "Melee", "Archer", "Tank", "GlassCannon").
  - `health`: The current health of the unit.
  - `coordinates`: A list containing the unit's x and y coordinates on the map (e.g., `[5, 10]`).
  - `goal`: This can be either a dictionary representing the unit's target (for attacking or gathering resources) or a list of coordinates for movement.

  Example `myUnits` entry:
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

- `myBuildings`: A list of dictionaries representing your buildings on the map. Each dictionary has the following keys:
  - `type`: The type of building (e.g., "Castle").
  - `health`: The current health of the building.
  - `coordinates`: A list containing the building's x and y coordinates on the map.

  Example `myBuildings` entry:
  ```python
  {
    "type": "Castle",
    "health": 100,
    "coordinates": [0, 0]
  }
  ```

- `trees`: A list of dictionaries representing the trees (resources) on the map. Each dictionary has the following keys:
  - `type`: The type of resource (e.g., "Tree").
  - `health`: The current health of the resource (determines how much can be gathered).
  - `coordinates`: A list containing the resource's x and y coordinates on the map.

  Example `trees` entry:
  ```python
  {
    "type": "Tree",
    "health": 10,
    "coordinates": [8, 12]
  }
  ```

- `enemyUnits`: A list of dictionaries representing the enemy's units on the map. The structure is the same as `myUnits`.
- `enemyBuildings`: A list of dictionaries representing the enemy's buildings on the map. The structure is the same as `myBuildings`.
- `wood`: The amount of wood resources you currently have.
- `stone`: The amount of stone resources you currently have.
- `summoncoords`: A list of coordinate lists where you can summon new units (e.g., `[[5, 8], [7, 10], ...]`).

## Request Object

The `Request` object is used to specify the action you want to take in the game. It has two properties:

- `gameObjectDict`: A dictionary representing the game object (unit or building) you want to act with. This dictionary should match one of the dictionaries in `myUnits` or `myBuildings`.

  Example `gameObjectDict`:
  ```python
  {
    "type": "Worker",
    "health": 15,
    "coordinates": [2, 5],
    "goal": None
  }
  ```

- `gameRequestDict`: A dictionary representing the request you want to make for the game object. This dictionary can have different structures depending on the type of request:

  - Movement request:
    ```python
    {
      "coordinates": [7, 12]
    }
    ```
    This request will move the specified unit or building to the given coordinates.

  - Attack request:
    ```python
    {
      "type": "Melee",
      "health": 18,
      "coordinates": [6, 9]
    }
    ```
    This request will make the specified unit or building attack the enemy unit or building at the given coordinates.

  - Resource gathering request:
    ```python
    {
      "type": "Tree",
      "health": 8,
      "coordinates": [10, 3]
    }
    ```
    This request will make the specified unit gather resources from the tree at the given coordinates.

  - Unit summoning request:
    ```python
    {
      "coordinates": [4, 6],
      "type": "Archer"
    }
    ```
    This request will summon a new Archer unit at the specified coordinates (if you have enough resources).

By combining the `gameObjectDict` and `gameRequestDict`, you can specify various actions for your units and buildings, such as moving, attacking, gathering resources, or summoning new units.

## Modifying the AI Strategy

To modify the AI strategy, you can edit the `playerAction` function in `player1.py` or `player2.py`. Here are some ideas for improvements:

1. **Resource Management**: Implement logic to balance the production of different unit types based on available resources and the game state.
2. **Unit Positioning**: Develop strategies for positioning units effectively, considering terrain, choke points, and defensive formations.
3. **Building Placement**: Decide where to place buildings strategically, considering resource locations and defensive positions.
4. **Scouting**: Incorporate scouting techniques to gather information about the enemy's units and buildings.
5. **Tactical Decisions**: Implement decision-making logic for when to attack, defend, or retreat based on the current game state.
6. **Advanced Pathfinding**: Improve unit movement by implementing advanced pathfinding algorithms that consider terrain, obstacles, and enemy units.

Remember, the more sophisticated your AI strategy, the better your chances of winning against other players in AlgoArena.