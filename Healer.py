import battlecode as bc

#takes a single healer
def healerWork(healer,c,gc):

    location = healer.location
    if location.is_on_map():
        nearby = gc.sense_nearby_units(location.map_location(), 7)
        close = gc.sense_nearby_units(location.map_location(), 5)

        #Find ally units within line of sight, and attempt to approach, unless they're also a healer.
        for target in nearby:
            if (target.team == healer.team) and (target.unit_type != bc.UnitType.Healer):
                # Find which direction to run in.
                d = bc.Direction
                if target.location.map_location().x == healer.location.map_location().x:
                    if target.location.map_location().y > healer.location.map_location().y:
                        direction = d.North
                    elif target.location.map_location().y < healer.location.map_location().y:
                        direction = d.South
                elif target.location.map_location().y == healer.location.map_location().y:
                    if target.location.map_location().x > healer.location.map_location().x:
                        direction = d.East
                    elif target.location.map_location().x < healer.location.map_location().x:
                        direction = d.West
                else:
                    if (target.location.map_location().x > healer.location.map_location().x) and (target.location.map_location().y > healer.location.map_location().y):
                        direction = d.Northeast
                    elif (target.location.map_location().x > healer.location.map_location().x) and (target.location.map_location().y < healer.location.map_location().y):
                        direction = d.Northwest
                    elif (target.location.map_location().x < healer.location.map_location().x) and (target.location.map_location().y > healer.location.map_location().y):
                        direction = d.Southeast
                    elif (target.location.map_location().x < healer.location.map_location().x) and (target.location.map_location().y < healer.location.map_location().y):
                        direction = d.Southwest
                # If healer can run in the chosen direction, run.
                if gc.is_move_ready(healer.id) and gc.can_move(healer.id, direction):
                    gc.move_robot(healer.id, direction)

        #Find units within "attack" range, and react accordingly.
        for target in close:
            # If they're a healable ally, heal them.
            if (target.team == healer.team) and (target.unit_type != bc.UnitType.Healer):
                # If it's close enough, and has the heat to heal or overcharge and ally, do so.
                if (gc.is_heal_ready (healer.id)) and (gc.can_heal(healer.id, target.id)):
                    gc.heal(healer.id, target.id)
                if (gc.is_overcharge_ready (healer.id)) and (gc.can_overcharge(healer.id, target.id)):
                    gc.overcharge(healer.id, target.id)

            # If it's an enemy, run.
            elif (target.team != healer.team) and (target.unit_type == bc.UnitType.Knight or bc.UnitType.Ranger or bc.UnitType.Mage):
                # Find which direction to run in.
                direction = bc.Direction
                if target.location.map_location().x == healer.location.map_location().x:
                    if target.location.map_location().y > healer.location.map_location().y:
                        direction = d.South
                    elif target.location.map_location().y < healer.location.map_location().y:
                        direction = d.North
                elif target.location.map_location().y == healer.location.map_location().y:
                    if target.location.map_location().x > healer.location.map_location().x:
                        direction = d.West
                    elif target.location.map_location().x < healer.location.map_location().x:
                        direction = d.East
                else:
                    if (target.location.map_location().x > healer.location.map_location().x) and (target.location.map_location().y > healer.location.map_location().y):
                        direction = d.Southwest
                    elif (target.location.map_location().x > healer.location.map_location().x) and (target.location.map_location().y < healer.location.map_location().y):
                        direction = d.Northwest
                    elif (target.location.map_location().x < healer.location.map_location().x) and (target.location.map_location().y > healer.location.map_location().y):
                        direction = d.Southeast
                    elif (target.location.map_location().x < healer.location.map_location().x) and (target.location.map_location().y < healer.location.map_location().y):
                        direction = d.Northeast
                # If healer can run in the chosen direction, run.
                if gc.is_move_ready(healer.id) and gc.can_move(healer.id, direction):
                    gc.move_robot(healer.id, direction)
    # Done turn.
    return True
