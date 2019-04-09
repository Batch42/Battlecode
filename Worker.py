import battlecode as bc
from random import shuffle

FACTORYSLOPE=100
ROCKETSLOPE=100
#takes a single worker
def workerWork(worker,c,gc):
    try:
        working = False
        location = worker.location
        if location.is_on_map():
            nearby = gc.sense_nearby_units(location.map_location(), 2)
            if worker.location.map_location().planet == bc.Planet.Earth:
                for thing in nearby:
                    if thing.unit_type == bc.UnitType.Rocket:
                        if gc.can_load(thing.id,worker.id):
                            gc.load(thing.id,worker.id)
                            return True
                # If it's a blueprint, build it.
                if gc.can_build(worker.id, thing.id):
                    gc.build(worker.id, thing.id)
                    working = True


                # If it's something in need of repair, repair it.
                elif gc.can_repair(worker.id, thing.id):
                    gc.repair(worker.id, thing.id)
                    working = True


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
            if gc.karbonite() > FACTORYSLOPE*c.factories:
                for directions in list(bc.Direction):
                    if gc.can_blueprint(worker.id, bc.UnitType.Factory, directions):
                        gc.blueprint(worker.id, bc.UnitType.Factory, directions)
                        working = True
            elif gc.karbonite() > ROCKETSLOPE*c.rockets:
                for directions in list(bc.Direction):
                    if gc.can_blueprint(worker.id, bc.UnitType.Rocket, directions):
                        gc.blueprint(worker.id, bc.UnitType.Rocket, directions)
                        working = True
            crowdcount=0

            # Otherwise, go harvest some resources.
            for direction in list(bc.Direction):
                if not gc.can_move(worker.id, direction):
                    crowdcount+=1
                if gc.can_harvest(worker.id, direction):
                    working = True
                    gc.harvest(worker.id, direction)
            #Get out of the way
            if crowdcount>4 or not working:
                deck=list(bc.Direction)
                shuffle(deck)
                for direction in deck:
                    if gc.is_move_ready(worker.id) and gc.can_move(worker.id, direction):
                        gc.move_robot(worker.id, direction)
                        break
            return True
    except Exception as e:
        print('Error:', e)
