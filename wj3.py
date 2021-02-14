"""
A variation on the class water jugs problem. Given three jugs J1,J2 and
J3 with capacities C1,C2 and C3, initially filled with water in amounts
W1,W2 and W3 liters.  Can you end up with exactly G1 liters in J1, G2 liters in J2 and G3 liters in J3?

Allowed actions: 
1. dump the contents of either jug onto the floor
2. pour the contents of one jug into the other until either the jug from which water is poured is empty or the one being filled is full 
3. filling any jug that is not yet full from a faucet until it is full.

The cost of each action is 1 plus the amount of water it uses (if any)
from the faucet.  For example, the action of emptying J1 costs 1, and
topping off J1 if it has capacity five liters but only two liters of
water costs 4.
"""

from search import Problem


class WJ3(Problem):
    """
    STATE: triples like (12,8,5) if jug J1 has 12 liters and J2 8 liters and J3 has 5 liters
    GOAL: a state except with 0 representing a 'don't care', so
      valid goals include (1,1,1) and (0,2,0).
    PROBLEM: Specify capacities of each jug, initial state and goal """

    def __init__(self, capacities=(12,8,5), initial=(0,0,0), goal=(6,0,0)):
        self.capacities = capacities
        self.initial = initial
        self.goal = goal

    def __repr__(self):
        """ Returns a string representing the object """
        return "WJ3({},{},{})".format(self.capacities, self.initial, self.goal)

    def goal_test(self, state):
        """ Returns True iff state is a goal state """
        G0,G1,G2 = self.goal
        return ((state[0]==G0 or G0==0) and 
            (state[1]==G1 or G1==0) and 
            (state[2]==G2 or G2==0))
    def h(self, node):
        """ Estimate of cost of shortest path from node to a goal """
        # heuristic function that estimates distance
        # to a goal node
        g = self.goal 
        if self.goal_test(node.state):
            return 0
        else:
            delta = sum(self.goal) - sum(node.state)
            return max(1, delta)    

    def actions(self, state):
        """ generates legal actions for state """
        (J0, J1, J2) = state
        """ generates legal actions for state """
        (C0, C1, C2) = self.capacities
        if J0 > 0: yield 'dump:0'
        if J1 > 0: yield 'dump:1'
        if J2 > 0: yield 'dump:2'

        if J0 < C0: yield 'fill:0'
        if J1 < C1: yield 'fill:1'
        if J2 < C2: yield 'fill:2'

        if J1<C1 and J0>0: yield 'pour:0-1'
        if J0<C0 and J1>0: yield 'pour:1-0'
        if J2<C2 and J0>0: yield 'pour:0-2'
        if J0<C0 and J2>0: yield 'pour:2-0'
        if J1<C1 and J2>0: yield 'pour:2-1'
        if J2<C2 and J1>0: yield 'pour:1-2'
        

    def result(self, state, action):
        """ Returns the successor of state after doing action """
        (J0, J1, J2) = state
        (C0, C1, C2) = self.capacities
        if action == 'dump:0': 
            return (0,J1,J2)
        elif action == 'dump:1': 
            return (J0,0,J2)
        elif action == 'dump:2': 
            return (J0,J1,0)
        elif action == 'pour:0-1': 
            delta = min(J0, C1-J1)
            return (J0-delta, J1+delta,J2)
        elif action == 'pour:1-0':
            delta = min(J1, C0-J0) 
            return (J0+delta, J1-delta,J2)
        elif action == 'pour:0-2': 
            delta = min(J0, C2-J2)
            return (J0-delta, J1,J2+delta)
        elif action == 'pour:2-0':
            delta = min(J2, C0-J0) 
            return (J0+delta, J1,J2-delta)
        elif action == 'pour:1-2': 
            delta = min(J1, C2-J2)
            return (J0,J1-delta, J2+delta)
        elif action == 'pour:2-1':
            delta = min(J2, C1-J1) 
            return (J0, J1+delta, J2-delta)
        elif action == 'fill:0':
            return (C0,J1,J2) 
        elif action == 'fill:1':
            return (J0,C1,J2) 
        elif action == 'fill:2':
            return (J0,J1,C2)
        raise ValueError('Unrecognized action: ' + action)

    def reachable_states(self):
        """Returns a set of the states that can be reached from the initial state"""
        seen = set()
        fringe = [self.initial]
        while fringe:
            print("fringe is:")
            print(fringe)
            state = fringe.pop(0)
            print("state is:")
            print(state)
            seen.add(state)
            print("seen is:")
            print(seen)
            for action in self.actions(state):
                print("action is:")
                print(action)
                new_state = self.result(state, action)
                print(new_state)
                if new_state not in seen and new_state not in fringe:
                    fringe.append(new_state)
        print("Final seen")
        print(seen)
        return seen

        
    def path_cost(self, c, state1, action, state2):
        """ Cost of path from start node to state1 assuming cost c to
        get to state1 and doing action to get to state2 """
        (C0, C1, C2) = self.capacities
        if action == 'fill:0':
           c += C0-state1[0]
        elif action == 'fill:1':
           c += C1-state1[1]
        elif action == 'fill:2':
           c += C2-state1[2]
        return c+1

 


def print_solution(solution):
    """If a path to a goal was found, prints the cost and the sequence of actions
    and states on a path from the initial state to the goal found"""
    if not solution:
        print("No solution found 🙁")
    else:
        print("Path of cost", solution.path_cost, end=': ')
        for node in solution.path():
              if not node.action:  # None implies it's the initial state
                  print(node.state, end=' ')
              else:
                  print('--{}--> {}'.format(node.action, node.state), end=' ')

