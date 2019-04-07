import battlecode as bc
gc = bc.GameController()

#takes a single healer
def healerWork(healer):
    try:
        location = healer.location
        if location.is_on_map():
            nearby = gc.sense_nearby_units(location.map_location(), 50)
            close = gc.sense_nearby_units(location.map_location(), 30)

            #Find ally units within line of sight, and attempt to approach, unless they're also a healer.
            for target in nearby:
                if (target.team == healer.team) and (target.unit_type != bc.UnitType.healer):
                    # Find which direction to run in.
                    direction = bc.Direction
                    if target.x == healer.x:
                        if target.y > healer.y:
                            direction = North
                        elif target.y < healer.y:
                            direction = South
                    elif target.y == healer.y:
                        if target.x > healer.x:
                            direction = East
                        elif target.x < healer.x:
                            direction = West
                    else:
                        if (target.x > healer.x) and (target.y > healer.y):
                            direction = Northeast
                        elif (target.x > healer.x) and (target.y < healer.y):
                            direction = Northwest
                        elif (target.x < healer.x) and (target.y > healer.y):
                            direction = Southeast
                        elif (target.x < healer.x) and (target.y < healer.y):
                            direction = Southwest
                    # If healer can run in the chosen direction, run.
                    if gc.is_move_ready(healer.id) and gc.can_move(healer.id, direcion):
                        gc.move_robot(healer.id, direction)
                    
            #Find units within "attack" range, and react accordingly.       
            for thing in close:    
                # If they're a healable ally, heal them.
                if (thing.team == healer.team) and (thing.unit_type != UnitType.Healer):
                    # If it's close enough, and has the heat to heal or overcharge and ally, do so.
                    if (gc.is_heal_ready (healer.id)) and (gc.can_heal(healer.id, thing.id)):
                        gc.heal(healer.id, thing.id)
                    if (gc.is_overcharge_ready (healer.id)) and (gc.can_overcharge(healer.id, thing.id)):
                        gc.overcharge(healer.id, thing.id)

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
                    # If healer can run in the chosen direction, run.
                    if gc.is_move_ready(healer.id) and gc.can_move(healer.id, direcion):
                        gc.move_robot(healer.id, direction)
    # Done turn.
    return True

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

