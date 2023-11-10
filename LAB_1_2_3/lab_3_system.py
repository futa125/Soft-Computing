from LAB_1_2_3.boat.inputvalues import InputValues
from LAB_1_2_3.defuzzify.coa import COADefuzzifier
from LAB_1_2_3.defuzzify.defuzzify import Defuzzifier
from LAB_1_2_3.fuzzy_system.accelerator import AcceleratorFuzzySystem
from LAB_1_2_3.fuzzy_system.fuzzy_system import FuzzySystem
from LAB_1_2_3.fuzzy_system.rudder import RudderFuzzySystem
from LAB_1_2_3.rule.rule import Rule


def main() -> None:
    defuzzifier: Defuzzifier = COADefuzzifier()
    rudder: FuzzySystem = RudderFuzzySystem(defuzzifier)
    accelerator: FuzzySystem = AcceleratorFuzzySystem(defuzzifier)

    fuzzy_system: FuzzySystem

    while True:
        rule: Rule
        fuzzy_system_selection = input("Select rule set (1=Rudder, 2=Accelerator): ")
        if int(fuzzy_system_selection) == 1:
            fuzzy_system = rudder
        elif int(fuzzy_system_selection) == 2:
            fuzzy_system = accelerator
        else:
            raise ValueError

        input_values = input("Enter input values (L, D, LK, DK, V, S): ")

        values = InputValues(*[int(x) for x in input_values.split(" ")])

        print(fuzzy_system.generate_results(values))
        print(fuzzy_system.decide(values))


if __name__ == "__main__":
    main()
