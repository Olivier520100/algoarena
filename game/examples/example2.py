from gameRequests import Request

from player import Player

import random



def playerAction(player: Player):

    castlehealth = player.myBuildings[0]['health']

    print(f"Wood: {player.wood}, Stone: {player.stone}, Unit Count: {len(player.myUnits)} Castle Health: {castlehealth}")

    randomcoords = player.summoncoords[random.randint(0,len(player.summoncoords)-1)]



    randomcoords = random.choice(player.summoncoords)

    # Process each unit's actions

    for unit in player.myUnits:

        if unit['type'] == 'Melee' or unit['type'] == 'Archer' and unit['goal'] is None:

            # Target the nearest enemy worker for Melee units without a goal

            closest_tree = None

            min_distance = float('inf')

            for tree in player.enemyUnits:

                distance = ((unit['coordinates'][0] - tree['coordinates'][0]) ** 2 + 

                            (unit['coordinates'][1] - tree['coordinates'][1]) ** 2) ** 0.5

                if distance < min_distance:

                    min_distance = distance

                    closest_tree = tree



            if closest_tree:

                return Request(unit, closest_tree)

            else:

                return Request(unit,player.enemyBuildings[0])





        if unit['type'] == 'Worker' and unit['goal'] is None:

            # Find the closest tree for the Worker to gather from

            closest_tree = None

            min_distance = float('inf')

            for tree in player.trees:

                distance = ((unit['coordinates'][0] - tree['coordinates'][0]) ** 2 + 

                            (unit['coordinates'][1] - tree['coordinates'][1]) ** 2) ** 0.5

                if distance < min_distance:

                    min_distance = distance

                    closest_tree = tree



            if closest_tree:

                return Request(unit, closest_tree)

                

    if len([unit for unit in player.enemyUnits if unit['type'] == 'Worker']) < 5:

        return Request(player.myBuildings[0], {"coordinates": randomcoords, "type": "Worker"})

    else:

        # Genere au hasard un archer ou un melee
        random_number = random.randint(0,1)

        if random_number is 1:
            return Request(player.myBuildings[0], {"coordinates": randomcoords, "type": "Archer"})
        else:
            return Request(player.myBuildings[0], {"coordinates": randomcoords, "type": "Melee"})

