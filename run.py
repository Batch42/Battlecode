import battlecode as bc
import sys
import Worker
import Ranger
import Econ

gc = bc.GameController()
dirs = list(bc.Direction)

while True:
    try:
        for unit in gc.my_units():
            if unit.unit_type()==UnitType.Worker:
                Worker.workerWork(unit)
            if unit.unit_type()==UnitType.Ranger:
                Ranger.rangerWork(unit)
            if unit.unit_type()==UnitType.Factory:
                Econ.factoryWork(unit)

    except Exception as err:
        print(err)
    sys.stdout.flush()
    sys.stderr.flush()
    gc.next_turn()
