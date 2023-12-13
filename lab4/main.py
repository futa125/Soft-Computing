import math
import random
from abc import ABCMeta
from dataclasses import dataclass, field
from typing import List, NamedTuple


@dataclass
class Reading:
    x: float
    y: float
    out: float


class Parameters(NamedTuple):
    b0: float
    b1: float
    b2: float
    b3: float
    b4: float

    def __str__(self):
        return f"{self.b0:.10f}, {self.b1:.10f}, {self.b2:.10f}, {self.b3:.10f}, {self.b4:.10f}"


@dataclass
class Individual:
    params: Parameters
    loss: float


class TransferFunction:
    @staticmethod
    def value(x: float, y: float, params: Parameters) -> float:
        return (math.sin(params.b0 + params.b1 * x) + params.b2 * math.cos(x * (params.b3 + y)) *
                (1 / (1 + math.exp(math.pow(x - params.b4, 2)))))


@dataclass
class GeneticAlgorithm(metaclass=ABCMeta):
    population_size: int
    generations: int
    transfer_function: TransferFunction = field(default_factory=TransferFunction)
    mutation_rate: float = 0.20
    min_value: float = -4
    max_value: float = +4

    readings_file: str = "datasets/dataset1.txt"
    readings: List[Reading] = field(init=False, default_factory=list)

    def __post_init__(self):
        with open(self.readings_file, "r") as file:
            for line in file:
                x, y, out = line.split("\t")
                self.readings.append(Reading(float(x), float(y), float(out)))

    def initial_population(self) -> List[Individual]:
        population: List[Individual] = []
        for _ in range(0, self.population_size):
            population.append(self.random_individual())

        return population

    def random_individual(self) -> Individual:
        b0, b1, b2, b3, b4 = (
            random.uniform(self.min_value, self.max_value),
            random.uniform(self.min_value, self.max_value),
            random.uniform(self.min_value, self.max_value),
            random.uniform(self.min_value, self.max_value),
            random.uniform(self.min_value, self.max_value),
        )

        params = Parameters(b0, b1, b2, b3, b4)

        return Individual(params, self.calculate_loss(params))

    @staticmethod
    def best_individual(population: List[Individual]) -> Individual:
        return min(population, key=lambda individual: individual.loss)

    @staticmethod
    def worst_individual(population: List[Individual]) -> Individual:
        return max(population, key=lambda individual: individual.loss)

    def calculate_loss(self, params: Parameters) -> float:
        value = 0
        for reading in self.readings:
            value += math.pow(self.transfer_function.value(reading.x, reading.y, params) - reading.out, 2)

        return value / len(self.readings)

    def tournament_selection(
            self, population: List[Individual], individuals_to_select: int, tournament_size: int = 5,
    ) -> List[Individual]:
        selected_individuals: List[Individual] = []
        for _ in range(individuals_to_select):
            tournament_individuals: List[Individual] = random.sample(population, tournament_size)
            selected_individuals.append(self.best_individual(tournament_individuals))

        return selected_individuals

    def cross(self, parent_a: Individual, parent_b: Individual) -> Individual:
        param_values: List[float] = []
        for param_a, param_b in zip(parent_a.params, parent_b.params):
            if random.randint(0, 1) == 0:
                param_values.append(param_a)
            else:
                param_values.append(param_b)

        params: Parameters = Parameters(*param_values)

        return Individual(params, self.calculate_loss(params))

    def mutate(self, individual: Individual) -> Individual:
        mutated_param_values: List[float] = []
        for param in individual.params:
            if random.random() < self.mutation_rate:
                mutated_param_values.append(random.uniform(self.min_value, self.max_value))
            else:
                mutated_param_values.append(param)

        mutated_params: Parameters = Parameters(*mutated_param_values)

        return Individual(mutated_params, self.calculate_loss(mutated_params))

    def run(self) -> Individual:
        raise NotImplementedError


@dataclass
class GenerationalGeneticAlgorithm(GeneticAlgorithm):
    generations: int = 1000
    population_size: int = 100
    use_elitism: bool = True

    def run(self) -> Individual:
        old_population: List[Individual] = self.initial_population()
        best_individual: Individual = self.best_individual(old_population)

        for i in range(0, self.generations):
            new_population: List[Individual] = []

            if self.use_elitism:
                new_population.append(self.best_individual(old_population))

            while len(new_population) != self.population_size:
                parent_a, parent_b = self.tournament_selection(old_population, 2)
                child = self.cross(parent_a, parent_b)
                child = self.mutate(child)

                new_population.append(child)

            if self.best_individual(new_population).loss < best_individual.loss:
                best_individual = self.best_individual(new_population)
                print(f"Generation: {i:10d}\tParameters: {best_individual.params}\tLoss: {best_individual.loss}")

            old_population = new_population

        return self.best_individual(old_population)


@dataclass
class SteadyStateGeneticAlgorithm(GeneticAlgorithm):
    generations: int = 100000
    population_size: int = 50

    def run(self) -> Individual:
        population: List[Individual] = self.initial_population()
        best_individual: Individual = self.best_individual(population)

        for i in range(0, self.generations):
            selection: List[Individual] = self.tournament_selection(population, 3)
            worst: Individual = self.worst_individual(selection)

            population.remove(worst)
            selection.remove(worst)

            child = self.cross(*selection)
            child = self.mutate(child)

            population.append(child)

            if self.best_individual(population).loss < best_individual.loss:
                best_individual = self.best_individual(population)
                print(f"Generation: {i:10d}\tParameters: {best_individual.params}\tLoss: {best_individual.loss}")

        return self.best_individual(population)


def main() -> None:
    generational_alg = GenerationalGeneticAlgorithm()
    steady_state_alg = SteadyStateGeneticAlgorithm()

    generational_alg.run()
    print()

    steady_state_alg.run()
    print()


if __name__ == "__main__":
    main()
