import util
import wordsegUtil

_X_ = None

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def start_state(self):
        # position before which text is reconstructed & previous word
        return 0, wordsegUtil.SENTENCE_BEGIN

	#0 현재까지 처리한 char수 / 이전까지 만들었던 단어의 수
	# 구현할 때는 loop를 2번 사용
	# loop 1개, space 쪼개는 곳, loop 1개 : candidate 조개는 부분 중 2중 loop

    def is_end(self, state):
        return state[0] == len(self.query)

    def succ_and_cost(self, state):
        pos, current_word = state
        for i in range(pos + 1, len(self.query)+1):
            vowel_removed_word = self.query[pos:i]
            fills = self.possibleFills(vowel_removed_word)
            for fill in fills:
                next_state = i,fill
                cost = self.bigramCost(current_word, fill)
                yield fill, next_state, cost  # return action, state, cost
	# use "self.possibleFills(vowel_removed_word)" instead of
	# "self.possilbeFills(vowel_removed_word)" | {vowel_removed_word}"
	#
	# user two ovelapped loops(중첩)

unigramCost, bigramCost = wordsegUtil.makeLanguageModels('leo-will.txt')
smoothCost = wordsegUtil.smoothUnigramAndBigram(unigramCost, bigramCost, 0.2)
possibleFills = wordsegUtil.makeInverseRemovalDictionary('leo-will.txt', 'aeiou')
problem = JointSegmentationInsertionProblem('mgnllthppl', smoothCost, possibleFills)

import dynamic_programming_search
dps = dynamic_programming_search.DynamicProgrammingSearch(verbose=1)
# dps = dynamic_programming_search.DynamicProgrammingSearch(memory_use=False, verbose=1)
# print(dps.solve(problem))

import uniform_cost_search
ucs = uniform_cost_search.UniformCostSearch(verbose=0)
print(ucs.solve(problem))
