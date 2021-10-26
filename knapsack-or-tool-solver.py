from ortools.algorithms import pywrapknapsack_solver
from pprint import pprint

import os
import time
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
    value_history = {}
    weight_history = {}
    optimal_history = {}
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    # Get test cases -> tc
    tc_path_tree = get_tc_path_tree(TC_PATH_ROOT)

    for tc_group in tc_path_tree.keys():

        base_history = {
            50: None,
            100 : None,
            200 : None,
            500 : None,
            1000 : None
        }
        value_history[tc_group] = base_history.copy()
        weight_history[tc_group] = base_history.copy()
        optimal_history[tc_group] = base_history.copy()

        for problem_path in tc_path_tree[tc_group]:
            problem_size, capacities, values, weights = get_info_tc(problem_path)
            can_solve = True
            if can_solve:
                solver.Init(values, weights, capacities)
                TIME_LIMIT = 60
                solver.set_time_limit( TIME_LIMIT )
                t0 = time.time()
                computed_value = solver.Solve()
                t = time.time() - t0

                packed_items = []
                packed_weights = []
                total_weight = 0                
                for i in range(len(values)):
                    if solver.BestSolutionContains(i):
                        # packed_items.append(i)
                        # packed_weights.append(weights[0][i])
                        total_weight += weights[0][i]
                # print('Total weight:', total_weight)
                # print('Packed items:', packed_items)
                # print('Packed_weights:', packed_weights)
                # history[tc_group][problem_size] = "v = " + str(computed_value) + ", w : " + str(total_weight)

                value_history[tc_group][problem_size] = str(computed_value)
                weight_history[tc_group][problem_size] = str(total_weight)
                if t > TIME_LIMIT:
                    optimal_history[tc_group][problem_size] = "_"
                else:
                    optimal_history[tc_group][problem_size] = "Optimal"
                
                value_df = pd.DataFrame(value_history)
                weight_df = pd.DataFrame(weight_history)
                optimal_df = pd.DataFrame(optimal_history)

                os.system('cls')

                print("Value table:")
                print(tabulate(value_df, headers='keys', tablefmt='psql'))
                value_df.to_csv("value.csv")

                print("Weight table:")
                print(tabulate(weight_df, headers='keys', tablefmt='psql'))
                weight_df.to_csv("weight.csv")

                print("Optimal table:")
                print(tabulate(optimal_df, headers='keys', tablefmt='psql'))
                optimal_df.to_csv("optimal.csv")

if __name__ == '__main__':
    main()
    