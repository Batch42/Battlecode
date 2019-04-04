import battlecode as bc
import sys
import Worker
import Ranger
import Econ
from Data import Counter

gc = bc.GameController()
dirs = list(bc.Direction)

while True:
    try:
        c = Counter()
        for unit in gc.my_units():
            if unit.unit_type()==UnitType.Worker:
                next.workers+=1
            if unit.unit_type()==UnitType.Ranger:
                next.rangers+=1
            if unit.unit_type()==UnitType.Factory:
                next.factories+=1 
           
        for unit in gc.my_units():
            if unit.unit_type()==UnitType.Worker:
                Worker.workerWork(unit,c)
            if unit.unit_type()==UnitType.Ranger:
                Ranger.rangerWork(unit,c)
            if unit.unit_type()==UnitType.Factory:
                Econ.factoryWork(unit,c)
        
    except Exception as err:
        print(err)
    sys.stdout.flush()
    sys.stderr.flush()
    gc.next_turn()
