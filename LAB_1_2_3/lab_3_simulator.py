import sys

from LAB_1_2_3.boat.inputvalues import InputValues
from LAB_1_2_3.defuzzify.coa import COADefuzzifier
from LAB_1_2_3.defuzzify.defuzzify import Defuzzifier
from LAB_1_2_3.fuzzy_system.accelerator import AcceleratorFuzzySystem
from LAB_1_2_3.fuzzy_system.fuzzy_system import FuzzySystem
from LAB_1_2_3.fuzzy_system.rudder import RudderFuzzySystem


def main() -> None:
    defuzzifier: Defuzzifier = COADefuzzifier()
    rudder: FuzzySystem = RudderFuzzySystem(defuzzifier)
    accelerator: FuzzySystem = AcceleratorFuzzySystem(defuzzifier)

    while True:
        input_values = input()
        if input_values == "KRAJ":
            break

        values = InputValues(*[int(x) for x in input_values.split(" ")])

        print(accelerator.decide(values), rudder.decide(values))

        sys.stdout.flush()


if __name__ == "__main__":
    main()
