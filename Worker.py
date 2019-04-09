import battlecode as bc
import random
# Derek's file so far.

# Priority list goes as such:
# Build up an adjacent blueprint
# Run from enemies
# Repair a damaged factory
# Build a rocket if it's appropriate
# Build a new factory
# Harvest karbonite
# Update karbonite map
# Move towards nearest karbonite

#takes a single worker
def workerWork(worker, c, gc, earth_karbonite_map, mars_karbonite_map):
    try:
        location = worker.location
        if location.is_on_map():
            nearby = gc.sense_nearby_units(location.map_location(), 2)
            for thing in nearby:
                # If it's a blueprint, build it.
                if gc.can_build(worker.id, thing.id):
                    gc.build(worker.id, thing.id)
                    # Done turn.
                    return True

                # If it's an enemy, run.
                elif (thing.team != worker.team) and (thing.unit_type == bc.UnitType.Knight or bc.UnitType.Ranger or bc.UnitType.Mage):
                    # Find which direction to run in.
                    direction = move_away_from_unit(worker, thing)
                    # If worker can run in the chosen direction, run.
                    if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direction):
                        gc.move_robot(worker.id, direction)
                        # Done turn.
                        return True

            nearby = gc.sense_nearby_units(location.map_location(), worker.vision_range)
            damaged = None
            damaged_distance = 0
            for thing in nearby:
                # If it's something in need of repair, repair it.
                if thing.unit_type == bc.UnitType.Factory and (thing.health < thing.max_health):
                    # Find the nearest thing in need of repair.
                    thing_distance = (abs(thing.location.map_location().x - worker.location.map_location().x) + abs(thing.location.map_location().y - worker.location.map_location().y))
                    if damaged is None or (thing_distance > damaged_distance):
                        damaged = thing
                        damaged_distance = thing_distance
                if damaged is not None:
                    if gc.can_repair(worker.id, thing.id):
                        gc.repair(worker.id, thing.id)
                        # Done turn.
                        return True
                    # Move towards the thing in need of repair.
                    else:
                        direction = move_towards(worker, damaged.location.map_location().x, damaged.location.map_location().y)
                        # If worker can move in the chosen direction, move.
                        if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direction):
                            gc.move_robot(worker.id, direction)
                            # Done turn.
                            return True

            # If a blueprint should be placed, place it.
            # If late enough in the game, try to build a rocket.
            if (c.turns >= 650) and c.rockets == 0:
                for directions in list(bc.Direction):
                    if gc.can_blueprint(worker.id, bc.UnitType.Rocket, directions):
                        gc.blueprint(worker.id, bc.UnitType.Rocket, directions)
                        c.rockets += 1
                        # Done turn.
                        return True
            # If have a sufficient buffer of karbonite, try to build a factory.
            if gc.karbonite() > 100 * c.factories:
                build_direction = bc.Direction
                can_build = True
                for directions in list(bc.Direction):
                    if not gc.can_blueprint(worker.id, bc.UnitType.Factory, directions):
                        can_build = False
                    else:
                        build_direction = directions
                if can_build and (gc.can_blueprint(worker.id, bc.UnitType.Factory, build_direction)):
                    gc.blueprint(worker.id, bc.UnitType.Factory, directions)
                    # Done turn.
                    return True

            # If resources are near, go harvest some resources.
            for directions in list(bc.Direction):
                if gc.can_harvest(worker.id, directions):
                    gc.harvest(worker.id, directions)
                    return True

            # If cannot harvest from an adjacent node, but the node comes up as harvestable on the map, update the map.
            # Do not return from this block.
            if worker.location.is_on_planet(bc.Planet.Earth):
                if not (worker.location.map_location().x + 1 >= len(earth_karbonite_map[worker.location.map_location().y])):
                    if earth_karbonite_map[worker.location.map_location().y][worker.location.map_location().x + 1] != 0 and gc.can_harvest(worker.id, bc.Direction.East) == False:
                        earth_karbonite_map[worker.location.map_location().y][worker.location.map_location().x + 1] = 0
                    if not (worker.location.map_location().y + 1 >= len(earth_karbonite_map)):
                        if earth_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x + 1] != 0 and gc.can_harvest(worker.id, bc.Direction.Northeast) == False:
                            earth_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x + 1] = 0
                    if not (worker.location.map_location().y - 1 <= 0):
                        if earth_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x + 1] != 0 and gc.can_harvest(worker.id, bc.Direction.Southeast) == False:
                            earth_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x + 1] = 0
                if not (worker.location.map_location().x - 1 < 0):
                    if earth_karbonite_map[worker.location.map_location().y][worker.location.map_location().x - 1] != 0 and gc.can_harvest(worker.id, bc.Direction.West) == False:
                        earth_karbonite_map[worker.location.map_location().y][worker.location.map_location().x - 1] = 0
                    if not (worker.location.map_location().y + 1 >= len(earth_karbonite_map)):
                        if earth_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x - 1] != 0 and gc.can_harvest(worker.id, bc.Direction.Northwest) == False:
                            earth_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x - 1] = 0
                    if not (worker.location.map_location().y - 1 < 0):
                        if earth_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x - 1] != 0 and gc.can_harvest(worker.id, bc.Direction.Southwest) == False:
                            earth_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x - 1] = 0
                if not (worker.location.map_location().y + 1 >= len(earth_karbonite_map)):
                    if earth_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x] != 0 and gc.can_harvest(worker.id, bc.Direction.North) == False:
                        earth_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x] = 0
                if not (worker.location.map_location().y - 1 < 0):
                    if earth_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x] != 0 and gc.can_harvest(worker.id, bc.Direction.South) == False:
                        earth_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x] = 0

            elif worker.location.is_on_planet(bc.Planet.Mars):
                if not (worker.location.map_location().x + 1 >= len(mars_karbonite_map[worker.location.map_location().y])):
                    if mars_karbonite_map[worker.location.map_location().y][worker.location.map_location().x + 1] != 0 and gc.can_harvest(worker.id, bc.Direction.East) == False:
                        mars_karbonite_map[worker.location.map_location().y][worker.location.map_location().x + 1] = 0
                    if not (worker.location.map_location().y + 1 >= len(mars_karbonite_map)):
                        if mars_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x + 1] != 0 and gc.can_harvest(worker.id, bc.Direction.Northeast) == False:
                            mars_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x + 1] = 0
                    if not (worker.location.map_location().y - 1 < 0):
                        if mars_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x + 1] != 0 and gc.can_harvest(worker.id, bc.Direction.Southeast) == False:
                            mars_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x + 1] = 0
                if not (worker.location.map_location().x - 1 < 0):
                    if mars_karbonite_map[worker.location.map_location().y][worker.location.map_location().x - 1] != 0 and gc.can_harvest(worker.id, bc.Direction.West) == False:
                        mars_karbonite_map[worker.location.map_location().y][worker.location.map_location().x - 1] = 0
                    if not (worker.location.map_location().y + 1 >= len(mars_karbonite_map)):
                        if mars_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x - 1] != 0 and gc.can_harvest(worker.id, bc.Direction.Northwest) == False:
                            mars_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x - 1] = 0
                    if not (worker.location.map_location().y - 1 < 0):
                        if mars_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x - 1] != 0 and gc.can_harvest(worker.id, bc.Direction.Southwest) == False:
                            mars_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x - 1] = 0
                if not (worker.location.map_location().y + 1 >= len(mars_karbonite_map)):
                    if mars_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x] != 0 and gc.can_harvest(worker.id, bc.Direction.North) == False:
                        mars_karbonite_map[worker.location.map_location().y + 1][worker.location.map_location().x] = 0
                if not (worker.location.map_location().y - 1 < 0):
                    if mars_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x] != 0 and gc.can_harvest(worker.id, bc.Direction.South) == False:
                        mars_karbonite_map[worker.location.map_location().y - 1][worker.location.map_location().x] = 0

            # Lastly, move towards the nearest karbonite deposit to try and gather from it.
            if gc.is_move_ready(worker.id):
                # Move towards the nearest karbonite deposit.
                nearest_karbonite_x = -1
                nearest_karbonite_y = -1
                nearest_karbonite_dist = -1

                # Checks the Earth map if on Earth
                if worker.location.map_location().planet == bc.Planet.Earth:
                    for y_node in range(0, len(earth_karbonite_map)):
                        for x_node in range(0, len(earth_karbonite_map[y_node])):
                            if earth_karbonite_map[y_node][x_node] > 0:
                                check_dist = (abs(x_node - worker.location.map_location().x) + abs(y_node - worker.location.map_location().y))
                                if (nearest_karbonite_dist == -1) or (nearest_karbonite_dist > check_dist):
                                    nearest_karbonite_x = x_node
                                    nearest_karbonite_y = y_node
                                    nearest_karbonite_dist = check_dist
                    direction = move_towards(worker, nearest_karbonite_x, nearest_karbonite_y)
                    if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direction):
                        gc.move_robot(worker.id, direction)
                        # Done turn.
                        return True

                # Checks the Mars map if on Mars
                elif worker.location.map_location().planet == bc.Planet.Mars:
                    for y_node in range(0, len(mars_karbonite_map)):
                        for x_node in range(0, len(mars_karbonite_map[y_node])):
                            if mars_karbonite_map[y_node][x_node] > 0:
                                check_dist = (abs(x_node - worker.location.map_location().x) + abs(y_node - worker.location.map_location().y))
                                if (nearest_karbonite_dist == -1) or (nearest_karbonite_dist > check_dist):
                                    nearest_karbonite_x = x_node
                                    nearest_karbonite_y = y_node
                                    nearest_karbonite_dist = check_dist
                    direction = move_towards(worker, nearest_karbonite_x, nearest_karbonite_y)
                    if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direction):
                        gc.move_robot(worker.id, direction)
                        # Done turn.
                        return True
                else:
                    gc.move_robot(worker.id, random.choice(list(bc.Direction)))
                    # Done turn.
                    return True

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

def move_away_from_unit (unit, run_from_unit):
    direction = bc.Direction
    if run_from_unit.location.map_location().x == unit.location.map_location().x:
        if run_from_unit.location.map_location().y > unit.location.map_location().y:
            direction = bc.Direction.South
        elif run_from_unit.location.map_location().y < unit.location.map_location().y:
            direction = bc.Direction.North
    elif run_from_unit.location.map_location().y == unit.location.map_location().y:
        if run_from_unit.location.map_location().x > unit.location.map_location().x:
            direction = bc.Direction.West
        elif run_from_unit.location.map_location().x < unit.location.map_location().x:
            direction = bc.Direction.East
    else:
        if (run_from_unit.location.map_location().x > unit.location.map_location().x) and (run_from_unit.location.map_location().y > unit.location.map_location().y):
            direction = bc.Direction.Southwest
        elif (run_from_unit.location.map_location().x > unit.location.map_location().x) and (run_from_unit.location.map_location().y < unit.location.map_location().y):
            direction = bc.Direction.Northwest
        elif (run_from_unit.location.map_location().x < unit.location.map_location().x) and (run_from_unit.location.map_location().y > unit.location.map_location().y):
            direction = bc.Direction.Southeast
        elif (run_from_unit.location.map_location().x < unit.location.map_location().x) and (run_from_unit.location.map_location().y < unit.location.map_location().y):
            direction = bc.Direction.Northeast
    return direction

def move_towards (unit, towards_x, towards_y):
    direction = bc.Direction
    if towards_x == unit.location.map_location().x:
        if towards_y > unit.location.map_location().y:
            direction = bc.Direction.North
        elif towards_y < unit.location.map_location().y:
            direction = bc.Direction.South
    elif towards_y == unit.location.map_location().y:
        if towards_x > unit.location.map_location().x:
            direction = bc.Direction.East
        elif towards_x < unit.location.map_location().x:
            direction = bc.Direction.West
    else:
        if (towards_x > unit.location.map_location().x) and (towards_y > unit.location.map_location().y):
            direction = bc.Direction.Northeast
        elif (towards_x > unit.location.map_location().x) and (towards_y < unit.location.map_location().y):
            direction = bc.Direction.Southeast
        elif (towards_x < unit.location.map_location().x) and (towards_y > unit.location.map_location().y):
            direction = bc.Direction.Northwest
        elif (towards_x < unit.location.map_location().x) and (towards_y < unit.location.map_location().y):
            direction = bc.Direction.Southwest
    return direction