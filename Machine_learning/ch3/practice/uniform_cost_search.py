import util

class UniformCostSearch(util.SearchAlgorithm):
    def __init__(self, verbose=0):
        self.verbose = verbose

    def solve(self, problem):
        numStatesExplored = 0

        # Initialize data structures
        frontier = util.PriorityQueue()  # Frontier states
        explored = set() # Explored states
        backpointers = {}  # map state to (action, previous state)
        frontier.update(problem.start_state(), 0)

        while not frontier.is_empty():            
            numStatesExplored += 1
            
            # Remove the state from the queue with the lowest priority.
            state, priority = frontier.remove_min()
            
            # Add state to explored
            explored.add(state)
            
            if self.verbose >= 2:
                print("Exploring %s with pastCost %s" % (state, priority))

            # Check if we've reached an end state; if so, extract solution.
            if problem.is_end(state):
                totalCost = priority
                actions = []
                while state != problem.start_state():
                    action, prevState = backpointers[state]
                    actions.append(action)
                    state = prevState
                actions.reverse()
                if self.verbose >= 1:
                    print("numStatesExplored = %d" % numStatesExplored)
                    print("totalCost = %s" % totalCost)
                    print("actions = %s" % actions)
                return actions, totalCost, numStatesExplored

            # Expand from |state| to new successor states,
            # updating the frontier with each newState.
            for action, newState, cost in problem.succ_and_cost(state):
                if self.verbose >= 3:
                    print("  Action %s => %s with cost %s + %s" % (action, newState, priority, cost))
                if newState not in explored:
                    # Found better way to go to |newState|, update backpointer.
                    new_priority = priority + cost
                    is_updated = frontier.update(newState, new_priority)
                    if is_updated:
                        backpointers[newState] = (action, state)
        if self.verbose >= 1:
            print("No path found")
            
        return None, None, numStatesExplored