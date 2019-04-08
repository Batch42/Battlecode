import battlecode as bc
fworkers=0
frangers=0
fhealers=0
#takes a single factory
def factoryWork(factory,c,gc):
    global fworkers, frangers, fhealers
    if factory.is_factory_producing():
        if factory.factory_unit_type()==bc.UnitType.Ranger:
            frangers+=1
        elif factory.factory_unit_type()==bc.UnitType.Healer:
            fhealers+=1
        else:
            fworkers+=1
    else:

        if len(factory.structure_garrison())>0:
            for d in list(bc.Direction):
                if gc.can_unload(factory.id,d):
                    gc.unload(factory.id,d)


        if fworkers*2>frangers:
            if gc.can_produce_robot(factory.id, bc.UnitType.Ranger):
                gc.produce_robot(factory.id, bc.UnitType.Ranger)
                frangers+=1
        elif fworkers*2>fhealers:
            if gc.can_produce_robot(factory.id, bc.UnitType.Healer):
                gc.produce_robot(factory.id, bc.UnitType.Healer)
                fhealers+=1
        else:
            if gc.can_produce_robot(factory.id, bc.UnitType.Worker):
                gc.produce_robot(factory.id, bc.UnitType.Worker)
                fworkers+=1

def resetFactory():
    global fworkers, frangers, fhealers
    fworkers=0
    frangers=0
    fhealers=0
