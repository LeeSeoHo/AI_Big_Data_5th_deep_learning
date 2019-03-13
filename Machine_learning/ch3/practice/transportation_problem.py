
import util

_X_ = None

class TransportationProblem(util.SearchProblem):
    def __init__(self, end_state):
        self.end_state = end_state

    def start_state(self):
        return 1

    def is_end(self, state):
        return state == self.end_state

    def succ_and_cost(self, state):
        results = []
        
        # Walk action
        if (state+1) <= self.end_state:
            next_state = state + 1
            action = 'Walk'
            cost = 1
            results.append((action, next_state, cost))
            
        # Tram action
        if (2*state) <= self.end_state:
            next_state = 2 * state
            action = 'Tram'
            cost = 2
            results.append((action, next_state, cost))
            
        return results

problem = TransportationProblem(7)

import backtracking_search
#bts = backtracking_search.BacktrackingSearch(verbose=3)
#print(bts.solve(problem))

import dynamic_programming_search
#dps = dynamic_programming_search.DynamicProgrammingSearch(verbose=1)
dps = dynamic_programming_search.DynamicProgrammingSearch(memory_use=True, verbose=1)
print(dps.solve(problem))

import uniform_cost_search
ucs = uniform_cost_search.UniformCostSearch(verbose=3)
# print(ucs.solve(problem))
