import battlecode as bc
from random import shuffle


def rocketWork(rocket,c,gc,marsx,marsy):
    if rocket.location.map_location().planet == bc.Planet.Earth and (len(rocket.structure_garrison())==rocket.structure_max_capacity() or gc.round==749):
        mars_map = gc.starting_map(bc.Planet.Mars)
        xlist = list(range(marsx))
        shuffle(xlist)
        for x in xlist:
            ylist = list(range(marsy))
            shuffle(ylist)
            for y in ylist:
                target = bc.MapLocation(bc.Planet.Mars,x,y)
                if mars_map.on_map(target):
                    if gc.can_launch_rocket(rocket.id,target):
                        if gc.has_unit_at_location(target):
                            if gc.sense_unit_at_location(target).team==rocket.team:
                                continue
                        gc.launch_rocket(rocket.id,target)
                        print("rocket launched")
    elif rocket.location.map_location().planet == bc.Planet.Mars:
        if len(rocket.structure_garrison())>0:
            for d in list(bc.Direction):
                if gc.can_unload(rocket.id,d):
                    gc.unload(rocket.id,d)


#takes a single factory
def factoryWork(factory,c,gc):
    if not factory.is_factory_producing():

        if(gc.karbonite()<200):

            return True

        if len(factory.structure_garrison())>0:
            for d in list(bc.Direction):
                if gc.can_unload(factory.id,d):
                    gc.unload(factory.id,d)


        if c.workers*2>c.rangers:
            if gc.can_produce_robot(factory.id, bc.UnitType.Ranger):
                gc.produce_robot(factory.id, bc.UnitType.Ranger)
        elif c.workers*2>c.healers:
            if gc.can_produce_robot(factory.id, bc.UnitType.Healer):
                gc.produce_robot(factory.id, bc.UnitType.Healer)
        else:
            if gc.can_produce_robot(factory.id, bc.UnitType.Worker):
                gc.produce_robot(factory.id, bc.UnitType.Worker)

def resetFactory():
    global fworkers, frangers, fhealers
    fworkers=0
    frangers=0
    fhealers=0
