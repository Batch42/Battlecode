import battlecode as bc
gc = bc.GameController()
# Derek's file so far.

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

                # If it's something in need of repair, repair it.
                elif gc.can_repair(worker.id, thing.id):
                    gc.repair(worker.id, thing.id)
                    # Done turn.
                    return True

                # If it's an enemy, run.
                elif (thing.team != worker.team) and (thing.unit_type == bc.UnitType.Knight or bc.UnitType.Ranger or bc.UnitType.Mage):
                    # Find which direction to run in.
                    direction = bc.Direction
                    if thing.x == worker.x:
                        if thing.y > worker.y:
                            direction = South
                        elif thing.y < worker.y:
                            direction = North
                    elif thing.y == worker.y:
                        if thing.x > worker.x:
                            direction = West
                        elif thing.x < worker.x:
                            direction = East
                    else:
                        if (thing.x > worker.x) and (thing.y > worker.y):
                            direction = Southwest
                        elif (thing.x > worker.x) and (thing.y < worker.y):
                            direction = Northwest
                        elif (thing.x < worker.x) and (thing.y > worker.y):
                            direction = Southeast
                        elif (thing.x < worker.x) and (thing.y < worker.y):
                            direction = Northeast
                    # If worker can run in the chosen direction, run.
                    if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direcion):
                        gc.move_robot(worker.id, direction)
                        # Done turn.
                        return True
            # If a blueprint should be placed, place it. <TODO> How many factories should we have at certain points in the game?
            if factory_count <= 6:
                for directions in list(bc.Direction):
                    if gc.can_blueprint(worker.id, UnitType.Factory, directions):
                        gc.blueprint(worker.id, UnitType.Factory, directions)
                        factory_count = factory_count + 1
                        return True
            # Otherwise, go harvest some resources.
            for directions in list(bc.Direction):
                if gc.can_harvest(worker.id, directions):
                    gc.harvest(worker.id, directions)
                    return True

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()
