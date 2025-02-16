import time

from algorithm.enhanced.core import tabu_search
from algorithm.enhanced.utils import val, soln_init


def run():

    num_runs: int = 100
    list_soln_best: list[int] = []
    list_soln_best_tracker: list[list[int]] = []
    exec_time = []

    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}")
        start = time.time()
        soln_best, soln_best_tracker = tabu_search(soln_init)
        end = time.time()
        exec_time.append(end - start)

        list_soln_best.append(soln_best)
        list_soln_best_tracker.append(soln_best_tracker)

    soln_lst = []
    for soln in list_soln_best:
        soln_lst.append(val(soln))
    soln_lst.sort()

    avg_soln = sum(soln_lst) / len(soln_lst)
    dif = ((max(soln_lst) - min(soln_lst)) / (sum(soln_lst) / len(soln_lst))) * 100
    avg_time = sum(exec_time) / len(exec_time)

    return avg_soln, dif, avg_time
