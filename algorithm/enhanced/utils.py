import math
import random
import pandas as pd
import time


distance_matrix: list[list[int]] = pd.read_csv("data/input/20.csv").values[:, 1:]

# Generate initial solution
soln_init: list[int] = list(range(distance_matrix.shape[0]))
random.shuffle(soln_init)


def val(soln: list[int]) -> int:
    """Calculate the value of the solution
    Args:
        soln: The solution
    Returns:
        value: The value of the solution
    Raises:
    """
    value: int = 0
    for i in range(len(soln) - 1):
        poi_first: int = soln[i]
        poi_second: int = soln[i + 1]
        value += distance_matrix[poi_first][poi_second]
    value += distance_matrix[-1][0]  # Back to starting POI

    return value


def dynamic_tenure(tabu_tenure, convergence_rate, stagnant_ctr, progress_ctr):

    # stagnation_threshold = math.ceil(len(soln_init) * 0.10)  # Dynamic threshold
    stagnation_threshold = 5

    # Reset
    if stagnant_ctr == 0:
        return math.floor(len(soln_init) * 0.10)

    # No improvement
    elif stagnant_ctr > 0 and stagnant_ctr < stagnation_threshold:
        return min(
            math.floor(len(soln_init) / 2),
            tabu_tenure + calculate_adjustment(convergence_rate),
        )

    # Continues no improvement
    elif stagnant_ctr >= stagnation_threshold:
        return min(
            math.floor(len(soln_init) / 2),
            tabu_tenure
            + calculate_adjustment(convergence_rate)
            + int(stagnant_ctr / 2),
        )


def calculate_adjustment(convergence_rate: float) -> int:
    """
    Calculate the adjustment amount for the tabu tenure based on the convergence rate.

    Args:
        convergence_rate: The current convergence rate.

    Returns:
        Adjustment amount as an integer.
    """
    if convergence_rate < 0.5:  # High convergence rate
        return 1  # Small adjustment for exploitation
    elif convergence_rate >= 0.9:  # Low convergence rate
        return 2  # Larger adjustment for exploration
    else:
        return 1  # Moderate adjustment


def neighborhood(soln: list[int], tabu_list: list[list[int]]) -> list[list[int]]:
    """Generates neighborhood of new solution from selected solution by
    making small changes.
    Args:
        soln: The current solution passed
        tabu_list: List of recent solutions
    Returns:
        nbhd: list of new solutions
    Raises:
    """
    nbhd: list = []
    for i in range(len(soln) - 1):
        for j in range(i + 1, len(soln)):
            soln_mod: list[int] = soln.copy()
            soln_mod[i], soln_mod[j] = soln_mod[j], soln_mod[i]
            nbhd.append(soln_mod)
    return nbhd


# OBJ1
def new_neighborhood(
    soln: list[int], tabu_list: list[list[int]], stagnant_ctr: int
) -> list[list[int]]:
    """Generates neighborhood of new solution from selected solution by
    making small changes. Perturbation is added when needed
    Args:
        soln: The current solution passed
        tabu_list: List of recent solutions
    Returns:
        nbhd: list of new solutions
    Raises:
    """

    if stagnant_ctr >= 5:
        for i in range(math.floor(stagnant_ctr / 5)):
            poi1_pos = random.randrange(len(soln))
            poi2_pos = random.randrange(len(soln))

            soln[poi1_pos] = soln[poi2_pos]
            soln[poi2_pos] = soln[poi1_pos]

    nbhd: list = []
    for i in range(len(soln) - 1):
        for j in range(i + 1, len(soln)):
            soln_mod: list[int] = soln.copy()
            soln_mod[i], soln_mod[j] = soln_mod[j], soln_mod[i]
            nbhd.append(soln_mod)
    return nbhd


def adaptive_stopping_criteria(stagnant_total: int, conv_ctr: int, time_start):

    stagnant_max: int = 10
    conv_max: int = 20
    max_time = 10

    if stagnant_total >= stagnant_max:
        return True

    #if conv_ctr >= conv_max:
    #    return True

    if (time_start - time.time()) >= max_time:
        return True

    return False


def best_admissible_soln(
    nbhd: list[list[int]], tabu_list: list[list[int]]
) -> list[int]:
    """Finds the best admissible solution. It must be better than current
    solution and doesn't exist in tabu list.
    Args:
        nbhd: Neighborhood of solutions
        tabu_list: List of recent solutions
    Returns:
        nbhr_best: Best admissible neighbor in the neighborhood
    Raises:
    """
    val_best: int = 100000  # Starts with large value to accept 1st neighbor
    nbhr_best: list[int] = None

    for nbhr_curr in nbhd:
        if nbhr_curr not in tabu_list:
            val_curr: int = val(nbhr_curr)
            if val_curr < val_best:
                val_best = val_curr
                nbhr_best = nbhr_curr

    return nbhr_best
