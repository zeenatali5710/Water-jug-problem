import sys
import argparse
import wj3 
import search as s

# default searchers from aima.search to use
default_searchers = [s.breadth_first_tree_search,
                     s.breadth_first_graph_search,
                     s.depth_first_graph_search,
                     s.iterative_deepening_search,
                     s.uniform_cost_search,
                     s.astar_search]

def wj3solve(capacities, start, goal, searchers=default_searchers):
    problem = wj3.WJ3(capacities, start, goal)
    print("Solving {}".format(problem))
    print('\nReachable states:', problem.reachable_states())
    for alg in searchers:
        print('\n\nSearch algorithm:', alg.__name__)
        wj3.print_solution(alg(problem))

    print("\n\nSUMMARY: successors/goal tests/states generated/solution")
    s.compare_searchers([problem], [], searchers)

def convert(args):
    """ Returns tuple (g1,g2,g3) after converting g1, g2 and g3 to integers"""
    return (int(args[0]), int(args[1]),int(args[2]))

def solve_all(plist):
    for capacities, start, goal in plist:
        print('**********************************************************************')
        try:
            wj3solve(capacities, start, goal)
        except:
            print('ERROR')
        print('\n')

# if called from the command line, call main()
if __name__ == "__main__":
    p = argparse.ArgumentParser(description='Test wj problem with several search algorithms')
    p.add_argument ('-c', '--capacities', nargs=3, type=int, default=(2,1,2))
    p.add_argument ('-s', '--start', nargs=3, type=int, default=(0,0,0))
    p.add_argument ('-g', '--goal', nargs=3, type=int, default=(1,0,0))
    args = p.parse_args()

    wj3solve(tuple(args.capacities), tuple(args.start), convert(tuple(args.goal)))


