import os
from dataclasses import dataclass, field
from typing import List

INPUT_PATH = "input"
OUTPUT_PATH = "output"


@dataclass(frozen=True)
class Street:
    start: int
    end: int
    name: str
    length: int


@dataclass(frozen=True)
class Car:
    visited_roads: List[str]


@dataclass(frozen=True)
class Problem:
    name: str
    simulation_time: int
    intersection_count: int
    street_count: int
    car_count: int
    destination_points: int
    streets: List[Street] = field(repr=False)
    cars: List[Car] = field(repr=False)


@dataclass(frozen=True)
class Solution:
    delivered_team_pizza: List[Street]  # TODO


def load_problem(filename: str):
    path = os.path.join(INPUT_PATH, filename)

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

        simulation_time, intersection_count, street_count, car_count, destination_points = lines[0].split()
        simulation_time, intersection_count, street_count, car_count, destination_points = int(simulation_time), int(
            intersection_count), int(street_count), int(car_count), int(destination_points)

        streets = []

        for street_index, line in enumerate(lines[1:1 + street_count]):
            start, end, name, length = line.split()
            streets.append(Street(start=int(start), end=int(end), name=name, length=int(length)))

        cars = []

        for car_index, line in enumerate(lines[1 + street_count:]):
            visited_roads = line.split()[1:]
            cars.append(Car(visited_roads=visited_roads))

        problem_name = filename[:-3]

        return Problem(
            name=problem_name,
            simulation_time=simulation_time,
            intersection_count=intersection_count,
            street_count=street_count,
            car_count=car_count,
            destination_points=destination_points,
            streets=streets,
            cars=cars,
        )


def load_problems():
    problems = []
    for filename in sorted(os.listdir(INPUT_PATH)):
        problems.append(load_problem(filename))

    return problems


def solve(problem: Problem):
    pass

    # return Solution()


def write_solution(problem: Problem, solution: Solution):
    pass
    # with open(os.path.join(OUTPUT_PATH, f"{problem.name}.out"), "w") as f:
    #     lines = list()
    #     lines.append(str(len(solution.delivered_team_pizza)))
    #
    #     for delivered_pizza_team in solution.delivered_team_pizza:
    #         pizza_indices = [str(pizza.index) for pizza in delivered_pizza_team.pizzas]
    #         pizza_indices_str = " ".join(pizza_indices)
    #         lines.append(f"{len(pizza_indices)} {pizza_indices_str}")
    #
    #     f.writelines(f"{line}\n" for line in lines)


def main():
    problems = load_problems()

    for problem in problems:
        print(f"Solving problem {problem.name}")

        print(problem)

        # solution = solve(problem)
        # write_solution(problem, solution)


if __name__ == '__main__':
    main()
