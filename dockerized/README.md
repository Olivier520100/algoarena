
# AlgoArena

AlgoArena is a platform for running game simulations between AI players and tracking their Elo ratings. It uses a Xata database to store user information, match details, and AI code. The game simulations are run in a secure environment using Docker containers to prevent accidental network access.

## Prerequisites

- Docker
- Python 3
- Xata account and database

## Setup


1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root directory with the following environment variables:

```
XATA_DATABASE_URL=<your_xata_database_url>
XATA_API_KEY=<your_xata_api_key>
```

Replace `<your_xata_database_url>` and `<your_xata_api_key>` with your actual Xata database URL and API key.

## Usage

1. Build the Docker image:

```bash
docker build -t algoarena .
```

2. Run the Docker container:

```bash
docker run -it algoarena
```

This will start the game simulation process, which follows these steps:

1. Retrieve user information from the Xata database.
2. Select two random users for the game simulation.
3. Check if a match between the selected users already exists in the database.
4. If no existing match is found, create a new match record.
5. Retrieve the AI code for the selected users from the database.
6. Write the AI code to `player1.py` and `player2.py` files.
7. Run the game simulation in a secure environment using Docker, preventing accidental network access.
8. Update the users' Elo ratings based on the game result.
9. Store the game result and video in the Xata database.

## Game AI

The game AI is implemented in the `player1.py` and `player2.py` files. These files are automatically updated with the AI code retrieved from the Xata database before each game simulation.

You can modify and update the AI code in the Xata database, and the changes will be reflected in the game simulations.

## Xata Database

The Xata database is used to store the following data:

- **Users**: Stores user information, including email, name, Elo rating, and AI code.
- **Matches**: Stores match details, including the participating users, winner, and game video.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
