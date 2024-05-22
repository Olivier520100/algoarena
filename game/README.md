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

To implement your AI strategy, modify the `playerAction` function in `player1.py` and `player2.py`. The function should return a `Request` object containing the desired action for a specific game object (unit or building) and the corresponding request (e.g., move, attack, summon).