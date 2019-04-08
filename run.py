import battlecode as bc
import sys
import Worker
import Ranger
import Econ
import Healer
from Data import Counter

gc = bc.GameController()
dirs = list(bc.Direction)

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

    for unit in gc.my_units():
        if unit.unit_type==bc.UnitType.Worker:
            Worker.workerWork(unit,c,gc)
        if unit.unit_type==bc.UnitType.Ranger:
            Ranger.rangerWork(unit,c,gc)
        if unit.unit_type==bc.UnitType.Factory:
            Econ.factoryWork(unit,c,gc)
        if unit.unit_type==bc.UnitType.Healer:
            Healer.healerWork(unit,c,gc)

    Econ.resetFactory()

    sys.stdout.flush()
    sys.stderr.flush()
    gc.next_turn()
