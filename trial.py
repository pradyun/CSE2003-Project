"""
"""

import satsolver


FILENAME = "trail1.sat.txt"


def main():
    with open(FILENAME) as f:
        instance = satsolver.Instance.from_file(f)

    solver = satsolver.SATSolver(instance)

    solutions = solver.recursive_solve()
    found_solution = False

    for satisfying_assignments in solutions:
        found_solution = True
        print(instance.assignment_to_string(
            satisfying_assignments, brief=False, starting_with=''
        ))

    if found_solution:
        print("SAT")
    else:
        print("UNSAT")

if __name__ == '__main__':
    main()
