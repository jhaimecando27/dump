import math
from algorithm.enhanced.utils import (
    neighborhood,
    new_neighborhood,
    best_admissible_soln,
    val,
    dynamic_tenure,
)

iter_max: int = 100


def tabu_search(soln_init: list[int]) -> tuple[list[int], list[int], list[int]]:
    """Tabu Search Algorithm
    Args:
        soln_init: Random initial solution
    Returns:
        soln_best: The best solution found by the TS algorithm
        soln_best_tracker: List of best solution in each iteration
    Raises:
    """

    # Tabu Search additional parameters
    tabu_list: list = []
    soln_curr: list[int] = soln_init
    soln_best: list[int] = soln_init

    prev_error: float = float("inf")

    # OBJ3
    poi_num = len(soln_init)
    tabu_tenure: int = math.floor(poi_num * 0.10)

    # Jupyter related
    stagnant_ctr: int = 0
    stagnant_total: int = 0
    progress_ctr: int = 0
    soln_best_tracker: list = []

    for iter_ctr in range(iter_max):

        # Find best neighbor
        # nbhd: list[list[int]] = neighborhood(soln_curr, tabu_list[: tabu_tenure - 1])
        nbhd: list[list[int]] = new_neighborhood(
            soln_curr, tabu_list[: tabu_tenure - 1], stagnant_ctr
        )
        nbhr_best: list[int] = best_admissible_soln(nbhd, tabu_list[: tabu_tenure - 1])
        if val(nbhr_best) < val(soln_best):
            soln_best = nbhr_best
            stagnant_ctr = 0
            progress_ctr += 1
        else:
            stagnant_ctr += 1
            progress_ctr = 0
            if stagnant_ctr == 10:
                stagnant_total += 1

        # Convergence Rate calculation
        curr_error = (
            abs(val(soln_best) - soln_best_tracker[-2])
            if len(soln_best_tracker) > 1
            else float("inf")
        )
        if prev_error > 0:
            convergence_rate = curr_error / prev_error
        prev_error = curr_error

        # Update tenure dynamically
        tabu_tenure = dynamic_tenure(
            tabu_tenure, convergence_rate, stagnant_ctr, progress_ctr
        )

        soln_curr = nbhr_best
        soln_best_tracker.append(val(soln_best))

        # Update Tabu List
        tabu_list.append(nbhr_best)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

    return soln_best, soln_best_tracker
