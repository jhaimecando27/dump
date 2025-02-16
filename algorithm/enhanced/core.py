import math
import time

from algorithm.enhanced.utils import (
    neighborhood,
    best_admissible_soln,
    val,
    dynamic_tenure,
    adaptive_stopping_criteria,
    new_neighborhood,
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
    time_start = time.time()

    prev_error: float = 0
    curr_error: float = 0
    conv_rate: float = 0
    conv_ctr: int = 0
    conv_treshold: float = 0.01

    # OBJ3
    poi_num = len(soln_init)
    tabu_tenure: int = math.floor(poi_num * 0.10)

    # Jupyter related
    stagnant_ctr: int = 0
    stagnant_total: int = 0
    progress_ctr: int = 0
    soln_best_tracker: list = []
    conv_rate_list: list = []

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
        if len(soln_best_tracker) >= 1:
            curr_error = val(soln_best) - soln_best_tracker[-1]

            if prev_error != 0:
                conv_rate = curr_error / prev_error
                conv_rate_list.append(conv_rate)

            if conv_rate <= conv_treshold:
                conv_ctr += 1

        prev_error = curr_error

        # Update tenure dynamically
        tabu_tenure = dynamic_tenure(tabu_tenure, conv_rate, stagnant_ctr, progress_ctr)

        soln_curr = nbhr_best
        soln_best_tracker.append(val(soln_best))

        # Update Tabu List
        tabu_list.append(nbhr_best)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

        #if adaptive_stopping_criteria(
        #    stagnant_total=stagnant_total, conv_ctr=conv_ctr, time_start=time_start
        #):
        #    break

    return soln_best, soln_best_tracker, conv_rate_list
