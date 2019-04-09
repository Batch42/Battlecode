import battlecode as bc
import sys
import Worker
import Ranger
import Econ
import Healer
from Data import Counter

gc = bc.GameController()
dirs = list(bc.Direction)

def find_map_limit(p, XorY):
    min = 19
    max = 49
    planet_map = gc.starting_map(p)
    increments = [20, 10, 5, 3, 2, 1]
    cur_inc = 0
    decrease = False

    while min != max - 1:
        tempmin = min + increments[cur_inc]
        if XorY == 'X':
            temp_location = bc.MapLocation(p, tempmin, 0)
        elif XorY == 'Y':
            temp_location = bc.MapLocation(p, 0, tempmin)

        if planet_map.on_map(temp_location):
            min = tempmin
        else:
            max = tempmin
            decrease = True
        if decrease:
            cur_inc += 1

    return min

def find_karbonite(planetmap, planet, Xcoords, Ycoords, map):
    for y in range(Ycoords+1):
        templist = []
        for x in range(Xcoords+1):
            temploc = bc.MapLocation(planet, x, y)
            if bc.PlanetMap.is_passable_terrain_at(planetmap, temploc):
                templist.append(bc.PlanetMap.initial_karbonite_at(planetmap, temploc))
            else:
                templist.append(0)
        map.append(templist)




EarthX = find_map_limit(bc.Planet.Earth, 'X')
EarthY = find_map_limit(bc.Planet.Earth, 'Y')
MarsX = find_map_limit(bc.Planet.Mars, 'X')
MarsY = find_map_limit(bc.Planet.Mars, 'Y')
earth_map = gc.starting_map(bc.Planet.Earth)
mars_map = gc.starting_map(bc.Planet.Mars)
earth_karbonite_map = []
mars_karbonite_map = []

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Ranger)
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Healer)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Ranger)

gc.queue_research(bc.UnitType.Healer)
gc.queue_research(bc.UnitType.Rocket)
#print(bc.PlanetMap.initial_karbonite_at(earth_map, temp_location))
find_karbonite(earth_map, bc.Planet.Earth, EarthX, EarthY, earth_karbonite_map)
find_karbonite(mars_map, bc.Planet.Mars, MarsX, MarsY, mars_karbonite_map)

while True:
    c = Counter()
    for unit in gc.my_units():
        if unit.unit_type==bc.UnitType.Worker:
            c.workers+=1
        if unit.unit_type==bc.UnitType.Ranger:
            c.rangers+=1
        if unit.unit_type==bc.UnitType.Factory:
            c.factories+=1
        if unit.unit_type==bc.UnitType.Healer:
            c.healers+=1
        if unit.unit_type==bc.UnitType.Rocket:
            c.rockets+=1

    for unit in gc.my_units():
        if unit.unit_type==bc.UnitType.Worker:
            Worker.workerWork(unit,c,gc, earth_karbonite_map, mars_karbonite_map)
        if unit.unit_type==bc.UnitType.Ranger:
            Ranger.rangerWork(unit,c,gc)
        if unit.unit_type==bc.UnitType.Factory:
            Econ.factoryWork(unit,c,gc)
        if unit.unit_type==bc.UnitType.Rocket:
            Econ.rocketWork(unit,c,gc,MarsX,MarsY)
        if unit.unit_type==bc.UnitType.Healer:
            Healer.healerWork(unit,c,gc)

    Econ.resetFactory()
    c.turns += 1
    
    sys.stdout.flush()
    sys.stderr.flush()
    gc.next_turn()
