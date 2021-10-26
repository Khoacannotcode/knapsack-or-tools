from ortools.algorithms import pywrapknapsack_solver
from pprint import pprint

import os
import pandas as pd
from tabulate import tabulate

# define test cases path
TC_PATH_ROOT = "kplib"

def get_tc_path_tree(TC_PATH_ROOT):
    tc_path_tree = dict()
    for _ in range(13):
        tc_path_tree[_] = []
    tc_group_list = os.listdir(TC_PATH_ROOT)
    tc_group_list.sort()
    # for tc_group in tc_group_list:
    for group_idx in range(len(tc_group_list)):
        tc_group = tc_group_list[group_idx]
        problem_size_list = os.listdir(os.path.join(TC_PATH_ROOT, tc_group))
        problem_size_list.sort()
        # Only solve problem with size in {50, 100, 200, 500, 1000}
        for problem_size in problem_size_list[:5]:
            tc_path = os.path.join(TC_PATH_ROOT, tc_group, problem_size, "R01000", "s000.kp")
            tc_path_tree[group_idx].append(tc_path)
    return tc_path_tree

def get_info_tc(tc_path):
    with open(tc_path, "r") as f:
        content = f.read()
    this_tc = content.split("\n")
    problem_size = int(this_tc[1])
    capacities = [int(this_tc[2])]
    values = []
    weights = [[]]
    for item in this_tc[4:-1]:
        value, weight = item.split(" ")
        values.append(int(value))
        weights[0].append(int(weight))
    return problem_size, capacities, values, weights

def main():
    # create history for saving results
    history = {}
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    # Get test cases -> tc
    tc_path_tree = get_tc_path_tree(TC_PATH_ROOT)

    for tc_group in tc_path_tree.keys():
        print("\n=========================")
        print("tc_group : ", tc_group)
        print("=========================")
        history[tc_group] = {
            50: None,
            100 : None,
            200 : None,
            500 : None,
            1000 : None
        }
        for problem_path in tc_path_tree[tc_group]:
            problem_size, capacities, values, weights = get_info_tc(problem_path)
            print("problem_size : ", problem_size)
            can_solve = True
            if can_solve:
                solver.Init(values, weights, capacities)
                solver.set_time_limit( 180 )
                computed_value = solver.Solve()

                packed_items = []
                packed_weights = []
                total_weight = 0
                # print('Total value =', computed_value)
                # if computed_value == pywrapknapsack_solver.OPTIMAL:
                #     history[tc_group][problem_size] = str(computed_value) + " Optimal"
                # else:
                #     history[tc_group][problem_size] = str(computed_value)
                history[tc_group][problem_size] = str(computed_value)
                df = pd.DataFrame(history)
                print(tabulate(df, headers='keys', tablefmt='psql'))
                df.to_csv("results.csv", index=False)
                # for i in range(len(values)):
                #     if solver.BestSolutionContains(i):
                #         # packed_items.append(i)
                #         # packed_weights.append(weights[0][i])
                #         total_weight += weights[0][i]
                # print('Total weight:', total_weight)
                # print('Packed items:', packed_items)
                # print('Packed_weights:', packed_weights)
                print("--------------------------")


if __name__ == '__main__':
    main()
    