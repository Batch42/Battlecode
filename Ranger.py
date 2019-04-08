import battlecode as bc
from random import shuffle
#takes a single ranger
def rangerWork(ranger,c,gc):
    location = ranger.location
    if location.is_in_garrison():
        return True
    nearby = gc.sense_nearby_units(location.map_location(), 50)
    for thing in nearby:
        if (thing.team != ranger.team) and gc.can_attack(ranger.id,thing.id):
            # Find which direction to withdraw.
            d = bc.Direction
            if thing.location.map_location().x == ranger.location.map_location().x:
                if thing.location.map_location().y > ranger.location.map_location().y:
                    direction = d.South
                elif thing.location.map_location().y < ranger.location.map_location().y:
                    direction = d.North
            elif thing.location.map_location().y == ranger.location.map_location().y:
                if thing.location.map_location().x > ranger.location.map_location().x:
                    direction = d.West
                elif thing.location.map_location().x < ranger.location.map_location().x:
                    direction =d.East
            else:
                if (thing.location.map_location().x > ranger.location.map_location().x) and (thing.location.map_location().y > ranger.location.map_location().y):
                    direction = d.Southwest
                elif (thing.location.map_location().x > ranger.location.map_location().x) and (thing.location.map_location().y < ranger.location.map_location().y):
                    direction = d.Northwest
                elif (thing.location.map_location().x < ranger.location.map_location().x) and (thing.location.map_location().y > ranger.location.map_location().y):
                    direction = d.Southeast
                elif (thing.location.map_location().x < ranger.location.map_location().x) and (thing.location.map_location().y < ranger.location.map_location().y):
                    direction = d.Northeast

            if gc.is_attack_ready(ranger.id):
                gc.attack(ranger.id,thing.id)
            # If ranger can retreat in the chosen direction, do so.
            if gc.is_move_ready(ranger.id) and gc.can_move(ranger.id, direction):
                gc.move_robot(ranger.id, direction)
            return True
    #Otherwise get out of the way
    deck=list(bc.Direction)
    shuffle(deck)
    for direction in deck:
        if gc.is_move_ready(ranger.id) and gc.can_move(ranger.id, direction):
            gc.move_robot(ranger.id, direction)
            break
    return True
