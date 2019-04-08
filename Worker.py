import battlecode as bc
import math
from random import shuffle
# Derek's file so far.

# Variables that need to be saved go here:
factory_count = 0

def check_direction(unit_x, unit_y, thing_x, thing_y):
    if unit_x == thing_x:
        if unit_y > thing_y:
            return bc.Direction.South
        elif unit_y < thing_y:
            return bc.Direction.North
    elif unit_y == thing_y:
        if unit_x > thing_x:
            return bc.Direction.West
        elif unit_x < thing_x:
            return bc.Direction.East
    else:
        if unit_x > thing_x and unit_y > thing_y:
            return bc.Direction.Southwest
        elif unit_x > thing_x and unit_y < thing_y:
            return bc.Direction.Northwest
        elif unit_x < thing_x and unit_y > thing_y:
            return bc.Direction.Southeast
        elif unit_x > thing_x and unit_y < thing_y:
            return bc.Direction.Northeast

#takes a single worker
def workerWork(worker, mapx, mapy, gc):
    cur_planet = None
    if worker.location.is_on_planet(bc.Planet.Earth):
        cur_planet = bc.Planet.Earth
    elif worker.location.is_on_planet(bc.Planet.Mars):
        cur_planet = bc.Planet.Mars
    #print("planet: ", cur_planet)
    global factory_count
    try:
        location = worker.location
        if location.is_on_map():
            nearby = gc.sense_nearby_units(location.map_location(), 2)
            for thing in nearby:
                # If it's a blueprint, build it.
                if gc.can_build(worker.id, thing.id):
                    gc.build(worker.id, thing.id)
                    # Done turn.


                # If it's something in need of repair, repair it.
                elif gc.can_repair(worker.id, thing.id):
                    gc.repair(worker.id, thing.id)
                    # Done turn.


                # If it's an enemy, run.
                elif (thing.team != worker.team) and (thing.unit_type == bc.UnitType.Knight or bc.UnitType.Ranger or bc.UnitType.Mage):
                    # Find which direction to run in.
                    d = bc.Direction
                    if thing.location.map_location().x == worker.location.map_location().x:
                        if thing.location.map_location().y > worker.location.map_location().y:
                            direction = d.South
                        elif thing.location.map_location().y < worker.location.map_location().y:
                            direction = d.North
                    elif thing.location.map_location().y == worker.location.map_location().y:
                        if thing.location.map_location().x > worker.location.map_location().x:
                            direction = d.West
                        elif thing.location.map_location().x < worker.location.map_location().x:
                            direction = d.East
                    else:
                        if (thing.location.map_location().x > worker.location.map_location().x) and (thing.location.map_location().y > worker.location.map_location().y):
                            direction = d.Southwest
                        elif (thing.location.map_location().x > worker.location.map_location().x) and (thing.location.map_location().y < worker.location.map_location().y):
                            direction = d.Northwest
                        elif (thing.location.map_location().x < worker.location.map_location().x) and (thing.location.map_location().y > worker.location.map_location().y):
                            direction = d.Southeast
                        elif (thing.location.map_location().x < worker.location.map_location().x) and (thing.location.map_location().y < worker.location.map_location().y):
                            direction = d.Northeast
                    # If worker can run in the chosen direction, run.
                    if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direction):
                        gc.move_robot(worker.id, direction)

            # If a blueprint should be placed, place it. <TODO> How many factories should we have at certain points in the game?
            if factory_count <= 6:
                for directions in list(bc.Direction):
                    if gc.can_blueprint(worker.id, bc.UnitType.Factory, directions):
                        gc.blueprint(worker.id, bc.UnitType.Factory, directions)
                        factory_count = factory_count + 1

            # Otherwise, go harvest some resources.
            for direction in list(bc.Direction):
                if gc.can_harvest(worker.id, direction):
                    gc.harvest(worker.id, direction)
                    print("Karbonite harvested!")
            #Get out of the way


            #If nothing above is satisfied, searches for nearest karbonite source
            if cur_planet != None:
                destination = None
                shortest_dist = 10000
                locations = gc.all_locations_within(worker.location.map_location(), 50)
                for loc in locations:
                    if bc.PlanetMap.is_passable_terrain_at(gc.starting_map(cur_planet), loc):
                        if gc.karbonite_at(loc) != 0:
                            diff = abs(loc.x - worker.location.map_location().x) + abs(loc.y - worker.location.map_location().y)
                            if diff < shortest_dist:
                                destination = loc
            #print("shouldn't be none: ", destination)
            if destination == None:
                worker_x = worker.location.map_location().x
                worker_y = worker.location.map_location().y
                dirs = []
                if worker_y < math.floor(2*mapy/3):
                    #TODO: insert code for seeking out Karbonite

            else:
                direction = check_direction(worker.location.map_location().x, worker.location.map_location().y, destination.x, destination.y)
                #print("destination: ", destination, " worker coords: ", worker.location.map_location().x, ",", worker.location.map_location().y, "direction: ", direction)
                if direction != None:
                    if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direction):
                        gc.move_robot(worker.id, direction)

            return True



            # dir = check_direction(worker.location.map_location().x, worker.location.map_location().y, 13, 13)
            # if gc.is_move_ready(worker.id) and gc.can_move(worker.id, dir):
            #     gc.move_robot(worker.id, dir)
            # return True

            # deck=list(bc.Direction)
            # shuffle(deck)
            # for direction in deck:
            #     if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direction):
            #         gc.move_robot(worker.id, direction)
            #         break

            #print("Worker ID: ", worker.id, " Worker coords: [", worker.location.map_location().x, ",", worker.location.map_location().y,']')
            return True

    except Exception as e:
        print('Error:', e)
        #traceback.print_exc()
