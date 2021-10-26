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
    # for tc_group in tc_group_list:
    for group_idx in range(len(tc_group_list)):
        tc_group = tc_group_list[group_idx]
        problem_size_list = os.listdir(os.path.join(TC_PATH_ROOT, tc_group))
        # Only solve problem with size in {50, 100, 200, 500, 1000}
        for problem_size in problem_size_list[:5]:
            tc_path = os.path.join(TC_PATH_ROOT, tc_group, problem_size, "R01000", "s000.kp")
            # print(tc_path)
            # with open(tc_path, "r") as f:
            #     content = f.read()
            #     # print(repr(content))
            #     problem_size, capacitiy, values, weights = get_tc_info(content)
            #     print("problem_size : ", problem_size)
            #     print("capabilitiy : ", capacitiy)
            #     print("values : ", values)
            #     print("weights : ", weights)
            # return
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
            # print("problem_size : ", problem_size)
            # print("capacities : ", capacities)
            # print("values : ", values)
            # print("weights : ", weights)
            # values = [
            #     360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
            #     78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
            #     87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
            #     312
            # ]
            # weights = [[
            #     7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
            #     42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
            #     3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13
            # ]]
            # capacities = [850]
            print("problem_size : ", problem_size)
            can_solve = True
            if can_solve:
                solver.Init(values, weights, capacities)
                computed_value = solver.Solve()

                packed_items = []
                packed_weights = []
                total_weight = 0
                print('Total value =', computed_value)
                history[tc_group][problem_size] = computed_value
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
    