import os
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict

INPUT_PATH = "input"
OUTPUT_PATH = "output"

DURATION = 1


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


@dataclass
class StreetGreenDuration:
    street_name: str
    duration: int


@dataclass
class Schedule:
    intersection_index: int
    street_green_duration: List[StreetGreenDuration]


@dataclass(frozen=True)
class Solution:
    schedules: List[Schedule]


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
    intersection_streets: Dict[int, List[Street]] = defaultdict(list)

    for street in problem.streets:
        intersection = street.end

        intersection_streets[intersection].append(street)

    schedules = []

    for intersection_index, incoming_streets in intersection_streets.items():
        street_green_duration = [StreetGreenDuration(street.name, DURATION) for street in
                                 incoming_streets]
        schedules.append(Schedule(intersection_index, street_green_duration))

    return Solution(schedules=schedules)


def write_solution(problem: Problem, solution: Solution):
    with open(os.path.join(OUTPUT_PATH, f"{problem.name}.out"), "w") as f:
        lines = list()

        lines.append(str(len(solution.schedules)))

        for schedule in solution.schedules:
            lines.append(str(schedule.intersection_index))
            lines.append(str(len(schedule.street_green_duration)))

            for street_green_duration in schedule.street_green_duration:
                lines.append(f"{street_green_duration.street_name} {street_green_duration.duration}")

        f.writelines(f"{line}\n" for line in lines)


def main():
    problems = load_problems()

    for problem in problems:
        print(f"Solving problem {problem.name}")

        solution = solve(problem)

        write_solution(problem, solution)


if __name__ == '__main__':
    main()
