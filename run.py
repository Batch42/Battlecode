import battlecode as bc
import random
import sys
import traceback
import math
import time
from datetime import datetime

'''
from worker import WorkerClass
from knight import KnightClass
from mage import MageClass
from healer import HealerClass
from ranger import RangerClass
from factory import FactoryClass
from rocket import RocketClass
from general import GeneralActions
'''

import os
print(os.getcwd())

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)

print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6137)

# let's start off with some research!
# we can queue as much as we want.
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()


class Worker_Actions(object):

    def search_karbonite(unit):
        for dir in directions:
            if gc.can_harvest(unit.id, dir):
                print("harvesting karbonite!")
                gc.harvest(unit.id, dir)
                break

    def self_replicate(unit):
        for dir in directions:
            if gc.can_replicate(unit.id, dir):
                print("performing mitosis!")
                gc.replicate(unit.id, dir)
                break


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


print('EarthX: ', EarthX, " EarthY: ", EarthY, " MarsX: ", MarsX, " MarsY: ", MarsY)
print(earth_map.on_map(bc.MapLocation(bc.Planet.Earth, EarthX, EarthY)))
temp_location = bc.MapLocation(bc.Planet.Earth, 0, 0)

#print(bc.PlanetMap.initial_karbonite_at(earth_map, temp_location))
find_karbonite(earth_map, bc.Planet.Earth, EarthX, EarthY, earth_karbonite_map)
for i in earth_karbonite_map:
    print(i)

#method that apprends amount of karbonite within each location to a 2D list with dimensions equivalent to the corresponding planet map
#input: the planet we're searching, the PlanetMap of the planet we're searching, the X and Y dimensions of said planet, the empty list we're appending to
#output: the amount of karbonite within each spot on the planet




#print(gc.PlanetMap.initial_karbonite_at(temp_location))



mars_deposits = []
earth_deposits = []











while True:
    # We only support Python 3, which means brackets around print()
    print('pyround:', gc.round(), 'time left:', gc.get_time_left_ms(), 'ms')


    # frequent try/catches are a good idea
    try:
        # walk through our units:
        for unit in gc.my_units():

            # first, factory logic
            if unit.unit_type == bc.UnitType.Factory:
                garrison = unit.structure_garrison()
                if len(garrison) > 0:
                    d = random.choice(directions)
                    if gc.can_unload(unit.id, d):
                        print('unloaded a worker!')
                        gc.unload(unit.id, d)
                        continue
                elif gc.can_produce_robot(unit.id, bc.UnitType.Worker):
                    gc.produce_robot(unit.id, bc.UnitType.Worker)
                    print('produced a worker!')
                    continue

            if unit.unit_type == bc.UnitType.Worker:
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, bc.Direction.North):
                    gc.move_robot(unit.id, bc.Direction.North)
                    print(unit.id, ' Moved north!')
                elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, bc.Direction.South):
                    gc.move_robot(unit.id, bc.Direction.South)
                    print(unit.id, ' Moved south!')
                #print('Moved successfully!')



            # if unit.unit_type == bc.UnitType.Knight:
            #     dir = random.choice(directions)
            #     if gc.is_move_ready(unit.id) and gc.can_move(unit.id, dir):
            #         gc.move_robot(unit.id, bc.Direction.North)



            # first, let's look for nearby blueprints to work on
            location = unit.location
            if location.is_on_map():
                nearby = gc.sense_nearby_units(location.map_location(), 2)
                for other in nearby:
                    if unit.unit_type == bc.UnitType.Worker and gc.can_build(unit.id, other.id):
                        gc.build(unit.id, other.id)
                        print('built a factory!')
                        # move onto the next unit
                        continue
                    if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                        print('attacked a thing!')
                        gc.attack(unit.id, other.id)
                        continue

            # okay, there weren't any dudes around
            # pick a random direction:
            d = random.choice(directions)

            # or, try to build a factory:
            if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                gc.blueprint(unit.id, bc.UnitType.Factory, d)
            # and if that fails, try to move
            elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)

    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
