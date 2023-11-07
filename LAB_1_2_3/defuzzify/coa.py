from LAB_1_2_3.defuzzify.defuzzify import Defuzzifier
from LAB_1_2_3.fuzzy_set.fuzzy_set import FuzzySetInterface


class COADefuzzifier(Defuzzifier):
    def defuzzify(self: Defuzzifier, fuzzy_set: FuzzySetInterface) -> float:
        centroid: float = 0
        area: float = 0

        for element in fuzzy_set.get_domain():
            centroid += fuzzy_set.get_value_at(element) * element.get_component_value(0)
            area += fuzzy_set.get_value_at(element)

        if area == 0:
            area = 1

        return centroid / area
