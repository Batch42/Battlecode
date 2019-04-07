import battlecode as bc
gc = bc.GameController()
# Derek's file so far.

# Priority list goes as such:
# Build up an adjacent blueprint
# Run from enemies
# Repair a damaged factory
# Build a new factory
# Harvest karbonite
# Move towards nearest karbonite

# Variables that need to be saved go here:
factory_count = 0

#takes a single worker
def workerWork(worker):
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
                    if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direcion):
                        gc.move_robot(worker.id, direction)
                        # Done turn.
                        return True

            nearby = gc.sense_nearby_units(location.map_location(), worker.vision_range) #TODO How the heck does ranges work?
            damaged = NULL
            damaged_distance = 0
            for thing in nearby:
                # If it's something in need of repair, repair it.
                if thing.unit_type == bc.UnitType.Factory and (thing.health < thing.max_health):
                    # Find the nearest thing in need of repair.
                    thing_distance = (abs(thing.x - worker.x) + abs(thing.y - worker.y))
                    if damaged == NULL or (thing_distance > damaged_distance):
                        damaged = thing
                        damaged_distance = thing_distance
                if damaged != NULL:
                    if gc.can_repair(worker.id, thing.id):
                        gc.repair(worker.id, thing.id)
                        # Done turn.
                        return True
                    # Move towards the thing in need of repair.
                    else:
                        direction = move_towards_unit(worker, damaged)
                        # If worker can move in the chosen direction, move.
                        if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direcion):
                            gc.move_robot(worker.id, direction)
                            # Done turn.
                            return True

            # If a blueprint should be placed, place it. TODO How many factories should we have at certain points in the game?
            # TODO factory_count might not be a variable, fix with proper variable name.
            if factory_count <= 6:
                for directions in list(bc.Direction):
                    if gc.can_blueprint(worker.id, UnitType.Factory, directions):
                        gc.blueprint(worker.id, UnitType.Factory, directions)
                        factory_count = factory_count + 1
                        return True
            # If resources are near, go harvest some resources.
            for directions in list(bc.Direction):
                if gc.can_harvest(worker.id, directions):
                    gc.harvest(worker.id, directions)
                    return True
            # Otherwise, move.
            if gc.is_move_ready(worker.id):
                # Move towards the nearest karbonite deposit. TODO How to find nearest karbonite, preferably without searching the whole tree.
                nearest_karbonite_x = -1
                nearest_karbonite_y = -1
                if .

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

def move_away_from_unit (unit, run_from_unit):
    direction = bc.Direction
    if run_from_unit.x == unit.x:
        if run_from_unit.y > unit.y:
            direction = South
        elif run_from_unit.y < unit.y:
            direction = North
    elif run_from_unit.y == unit.y:
        if run_from_unit.x > unit.x:
            direction = West
        elif run_from_unit.x < unit.x:
            direction = East
    else:
        if (run_from_unit.x > unit.x) and (run_from_unit.y > unit.y):
            direction = Southwest
        elif (run_from_unit.x > unit.x) and (run_from_unit.y < unit.y):
            direction = Northwest
        elif (run_from_unit.x < unit.x) and (run_from_unit.y > unit.y):
            direction = Southeast
        elif (run_from_unit.x < unit.x) and (run_from_unit.y < unit.y):
            direction = Northeast
    return direction

def move_towards_unit (unit, run_towards_unit):
    direction = bc.Direction
    if run_towards_unit.x == unit.x:
        if run_towards_unit.y > unit.y:
            direction = North
        elif run_towards_unit.y < unit.y:
            direction = South
    elif run_towards_unit.y == unit.y:
        if run_towards_unit.x > unit.x:
            direction = East
        elif run_towards_unit.x < unit.x:
            direction = West
    else:
        if (run_towards_unit.x > unit.x) and (run_towards_unit.y > unit.y):
            direction = Northeast
        elif (run_towards_unit.x > unit.x) and (run_towards_unit.y < unit.y):
            direction = Southeast
        elif (run_towards_unit.x < unit.x) and (run_towards_unit.y > unit.y):
            direction = Northwest
        elif (run_towards_unit.x < unit.x) and (run_towards_unit.y < unit.y):
            direction = Southwest
    return direction