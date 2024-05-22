from gameRequests import Request

from player import Player

import random


# Défini le tour du joueur
def playerAction(player: Player):

    castlehealth = player.myBuildings[0]['health']

    print(f"Wood: {player.wood}, Stone: {player.stone}, Unit Count: {len(player.myUnits)} Castle Health: {castlehealth}")

    randomcoords = player.summoncoords[random.randint(0,len(player.summoncoords)-1)]

    randomcoords = random.choice(player.summoncoords)





    # Instructions pour chaque type d'unités

    for unit in player.myUnits:

        if unit['type'] == 'Archer' and unit['goal'] is None:

            # Attaque tout sauf les travailleurs ennemis

            closest_enemy = None

            min_distance = float('inf')

            for enemy in player.enemyUnits:

                if enemy['type'] != 'Worker': 

                    distance = ((unit['coordinates'][0] - tree['coordinates'][0]) ** 2 + 

                                (unit['coordinates'][1] - tree['coordinates'][1]) ** 2) ** 0.5

                    if distance < min_distance:

                        min_distance = distance

                        closest_enemy = enemy

            if closest_enemy:

                return Request(unit, closest_enemy)

            else:

                return Request(unit,player.enemyBuildings[0])

        if unit['type'] == 'Melee' and unit['goal'] is None:

            # Attaque les travailleurs ennemis uniquement

            closest_enemy = None

            min_distance = float('inf')

            for enemy in player.enemyUnits:

                if unit['type'] == 'Worker': 

                    distance = ((unit['coordinates'][0] - tree['coordinates'][0]) ** 2 + 

                                (unit['coordinates'][1] - tree['coordinates'][1]) ** 2) ** 0.5

                    if distance < min_distance:

                        min_distance = distance

                        closest_enemy = enemy


            if closest_enemy:

                return Request(unit, closest_enemy)

            else:

                return Request(unit,player.enemyBuildings[0])



        if unit['type'] == 'Worker' and unit['goal'] is None:

            # Cherche l'arbre le plus proche à collecter

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

                
    # Instructions pour décider quel type d'unité produire
    if player.wood <= 60:

        return Request(player.myBuildings[0], {"coordinates": randomcoords, "type": "Worker"})

    elif any([unit for unit in player.enemyUnits if unit['type'] == 'Melee']) or any([unit for unit in player.enemyUnits if unit['type'] == 'Archer']):

        # produit des archers seulement s'il y a des unités de combat dans l'équipe adverse
    
        return Request(player.myBuildings[0], {"coordinates": randomcoords, "type": "Archer"})
    
    elif len([unit for unit in player.enemyUnits if unit['type'] == 'Worker']) > len([unit for unit in player.myUnits if unit['type'] == 'Melee']):

        # produit des mélées seulement s'il y a des travailleurs dans l'équipe adverse
        
        return Request(player.myBuildings[0], {"coordinates": randomcoords, "type": "Melee"})

