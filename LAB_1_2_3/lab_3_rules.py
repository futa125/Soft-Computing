from LAB_1_2_3.boat.inputvalues import InputValues
from LAB_1_2_3.defuzzify.coa import COADefuzzifier
from LAB_1_2_3.defuzzify.defuzzify import Defuzzifier
from LAB_1_2_3.fuzzy_system.accelerator import AcceleratorFuzzySystem, RULES as ACCELERATOR_RULES
from LAB_1_2_3.fuzzy_system.fuzzy_system import FuzzySystem
from LAB_1_2_3.fuzzy_system.rudder import RudderFuzzySystem, RULES as RUDDER_RULES
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
            for rule in RUDDER_RULES:
                print(rule)

            rule_selection = input("Select rule: ")
            rule = RUDDER_RULES[int(rule_selection)]

        elif int(fuzzy_system_selection) == 2:
            fuzzy_system = accelerator
            for rule in ACCELERATOR_RULES:
                print(rule)

            rule_selection = input("Select rule: ")
            rule = ACCELERATOR_RULES[int(rule_selection)]

        else:
            raise ValueError

        input_values = input("Enter input values (L, D, LK, DK, V, S): ")

        values = InputValues(*[int(x) for x in input_values.split(" ")])

        fuzzy_system.rules = [rule]

        print(fuzzy_system.generate_results(values))
        print(fuzzy_system.decide(values))


if __name__ == "__main__":
    main()
