import util
import wordsegUtil

_X_ = None

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def start_state(self):
        return 0  # num of characters used to construct words

    def is_end(self, state):
        return state == len(self.query)

    def succ_and_cost(self, state):
        for step in range(1, len(self.query) - state + 1):
            next_state = state + step
            word = _X_  # constructed word
            cost = self.unigramCost(word)
            yield word, next_state, cost  # action, next_state, cost

unigramCost, bigramCost = wordsegUtil.makeLanguageModels('leo-will.txt')
problem = SegmentationProblem('thisisnotmybeautifulhouse', unigramCost)

import dynamic_programming_search
dps = dynamic_programming_search.DynamicProgrammingSearch(verbose=1)
# dps = dynamic_programming_search.DynamicProgrammingSearch(memory_use=False, verbose=1)
# print(dps.solve(problem))

import uniform_cost_search
ucs = uniform_cost_search.UniformCostSearch(verbose=0)
print(ucs.solve(problem))
