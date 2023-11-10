import sys
import time

from LAB_1_2_3.boat.inputvalues import InputValues
from LAB_1_2_3.defuzzify.coa import COADefuzzifier
from LAB_1_2_3.defuzzify.defuzzify import Defuzzifier
from LAB_1_2_3.fuzzy_system.fuzzy_system import FuzzySystem
from LAB_1_2_3.fuzzy_system.rudder import RudderFuzzySystem
from LAB_1_2_3.fuzzy_system.accelerator import AcceleratorFuzzySystem


def main() -> None:
    defuzzifier: Defuzzifier = COADefuzzifier()
    rudder: FuzzySystem = RudderFuzzySystem(defuzzifier)
    accelerator: FuzzySystem = AcceleratorFuzzySystem(defuzzifier)

    while True:
        values = InputValues(*[int(x) for x in input().split(" ")])

        print(accelerator.decide(values), rudder.decide(values))

        sys.stdout.flush()


if __name__ == "__main__":
    main()
