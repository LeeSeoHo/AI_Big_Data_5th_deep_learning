
class GraphProblem():
    def __init__(self, states, distances):
        self.states = states
        self.distances = distances

    def start_state(self):
        return 'S'

    def is_end(self, state):
        return state == 'G'

    def succ_and_cost(self, state):
        results = []
        for (prev_state, next_state), cost in list(distances.items()):
            if prev_state == state:
                action = state +'->'+next_state
                results.append((action, next_state, cost))
        return results
        
states = ['S', 'A', 'B', 'C', 'D', 'E', 'G']
distances = {
    ('S', 'A'): 1,
    ('A', 'B'): 3,
    ('A', 'C'): 1,
    ('B', 'D'): 3,
    ('C', 'D'): 1,
    ('C', 'G'): 2,
    ('D', 'G'): 3,
    ('D', 'E'): 4,
    ('S', 'G'): 12,
}

problem = GraphProblem(states, distances)

import backtracking_search
bts = backtracking_search.BacktrackingSearch(verbose=3)
# print(bts.solve(problem))

import dynamic_programming_search
dps = dynamic_programming_search.DynamicProgrammingSearch(verbose=1)
# dps = dynamic_programming_search.DynamicProgrammingSearch(memory_use=False, verbose=1)
# print(dps.solve(problem))

import uniform_cost_search
ucs = uniform_cost_search.UniformCostSearch(verbose=3)
# print(ucs.solve(problem))
