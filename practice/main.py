import os
from dataclasses import dataclass, field
from typing import List, FrozenSet

INPUT_PATH = "input"
OUTPUT_PATH = "output"


@dataclass(frozen=True)
class Pizza:
    index: int
    ingredients: FrozenSet[str]


@dataclass(frozen=True)
class TeamPizzas:
    pizzas: List[Pizza]


@dataclass(frozen=True)
class Problem:
    name: str
    pizza_count: int
    team_2_count: int
    team_3_count: int
    team_4_count: int

    pizzas: List[Pizza] = field(repr=False)


@dataclass(frozen=True)
class Solution:
    delivered_team_pizza: List[TeamPizzas]


def load_problem(filename: str):
    path = os.path.join(INPUT_PATH, filename)

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

        pizza_count, team_2_count, team_3_count, team_4_count = lines[0].split()

        pizzas = []

        for pizza_index, line in enumerate(lines[1:]):
            ingredients = line.split()[1:]
            pizzas.append(Pizza(pizza_index, frozenset(ingredients)))

        problem_name = filename[:-3]

        return Problem(problem_name, int(pizza_count), int(team_2_count), int(team_3_count), int(team_4_count), pizzas)


def load_problems():
    problems = []
    for filename in sorted(os.listdir(INPUT_PATH)):
        problems.append(load_problem(filename))

    return problems


def deliver_greedy(team_size: int, number_of_teams_left: int, pizzas_left: List[Pizza]):
    delivered_team_pizzas = []

    while number_of_teams_left > 0:
        next_pizzas = pizzas_left[:team_size]
        pizzas_left = pizzas_left[team_size:]

        if len(next_pizzas) == 4:
            delivered_team_pizzas.append(TeamPizzas(next_pizzas))
            number_of_teams_left -= 1
        else:
            # Not enough pizzas left to deliver to the whole team / at all, put back the undelivered pizzas to the list
            pizzas_left = next_pizzas + pizzas_left
            break

    return delivered_team_pizzas, pizzas_left


def solve(problem: Problem):
    team_2_left = problem.team_2_count
    team_3_left = problem.team_3_count
    team_4_left = problem.team_4_count

    pizzas_left = problem.pizzas

    all_delivered_team_pizzas = []

    delivered_pizzas, pizzas_left = deliver_greedy(4, team_4_left, pizzas_left)
    all_delivered_team_pizzas.extend(delivered_pizzas)

    delivered_pizzas, pizzas_left = deliver_greedy(3, team_3_left, pizzas_left)
    all_delivered_team_pizzas.extend(delivered_pizzas)

    delivered_pizzas, pizzas_left = deliver_greedy(2, team_2_left, pizzas_left)
    all_delivered_team_pizzas.extend(delivered_pizzas)

    return Solution(all_delivered_team_pizzas)


def write_solution(problem: Problem, solution: Solution):
    with open(os.path.join(OUTPUT_PATH, f"{problem.name}.out"), "w") as f:
        lines = list()
        lines.append(str(len(solution.delivered_team_pizza)))

        for delivered_pizza_team in solution.delivered_team_pizza:
            pizza_indices = [str(pizza.index) for pizza in delivered_pizza_team.pizzas]
            pizza_indices_str = " ".join(pizza_indices)
            lines.append(f"{len(pizza_indices)} {pizza_indices_str}")

        f.writelines(f"{line}\n" for line in lines)


def main():
    problems = load_problems()

    for problem in problems:
        print(f"Solving problem {problem.name}")
        solution = solve(problem)
        write_solution(problem, solution)


if __name__ == '__main__':
    main()
