import random
import util

_X_ = None

class RandomGridSearchProblem(util.SearchProblem):
    def __init__(self, num_rows, num_cols, blocks=None, num_blocks=None, use_heuristic=False):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.use_heuristic = use_heuristic
        self.init_state = (0, 0)
        self.end_state = (num_rows - 1, num_cols - 1)

        self.row_costs = tuple(random.randint(1, 9)
                              for _ in range(num_rows - 1))
        
        self.col_costs = tuple(random.randint(1, 9)
                              for _ in range(num_cols - 1))

        assert blocks or num_blocks
        if blocks:
            self.blocks = set(blocks)
        else:
            self.blocks = set(random.sample(
                [(r, c) for r in range(num_rows)
                 for c in range(num_cols)], num_blocks))
            self.blocks = self.blocks - {self.init_state, self.end_state}

        self.action_move_cost_tuples = (
            ('North', (-1, 0), lambda state: self.row_costs[state[0] - 1]),
            ('South', (1, 0), lambda state: self.row_costs[state[0]]),
            ('West', (0, -1), lambda state: self.col_costs[state[1] - 1]),
            ('East', (0, 1), lambda state: self.col_costs[state[1]]))
        # state = (row, col)

        def accumulate_cost(costs):
            acc_costs = [None] * (len(costs) + 1)
            acc_costs[-1] = 0
            for idx in reversed(list(range(len(costs)))):
                acc_costs[idx] = acc_costs[idx + 1] + costs[idx]
            return acc_costs

        self.h_row = accumulate_cost(self.row_costs)
        self.h_col = accumulate_cost(self.col_costs)

    def start_state(self):
        return self.init_state
        
    def is_end(self, state):
        return state == self.end_state
        
    def succ_and_cost(self, state):
        row, col = state
        results = []

        for action, move, cost_func in self.action_move_cost_tuples:
            r_move, c_move = move
            new_state = (new_row, new_col) = (row + r_move, col + c_move)

            if all((new_state not in self.blocks,
                    0 <= new_row, new_row < self.num_rows,
                    0 <= new_col, new_col < self.num_cols)):
                cost = cost_func(state)
                if self.use_heuristic:
                    cost += self.heuristic(new_state) - self.heuristic(state)
                results.append((action, new_state, cost))

        return results

    def heuristic(self, state):
        row, col = state
        return _X_  # use self.h_row, self.h_col

    def print_grid(self):
        grid_str = ''
        grid_str += '# # ' + ' # '.join(map(str, list(range(self.num_cols)))) + '\n'
        grid_str += '# *' + ' * '.join([''] + list(map(str, self.col_costs))) + ' *\n'
        for row in range(self.num_rows):
            nodes = []
            for col in range(self.num_cols):
                state = (row, col)
                if state in self.blocks:
                    node = 'x'
                elif state == self.init_state:
                    node = 's'
                elif state == self.end_state:
                    node = 'g'
                else:
                    node = '.'
                nodes.append(node)
            grid_str += str(row) + ' * ' + ' - '.join(nodes) + '\n'
            if row < self.num_rows - 1:
                grid_str += '# ' + str(self.row_costs[row]) + ' | '.join([''] + [' '] * (self.num_cols - 1)) + ' |\n'
        print(grid_str)


import uniform_cost_search
ucs = uniform_cost_search.UniformCostSearch(verbose=3)

# blocks = [(4, c) for c in range(2, 6)] + [(r, 6) for r in range(1, 4)] + [(4, 6)]
blocks = [(r, 2) for r in range(0, 4)] + [(r, 4) for r in range(3, 6)]

random.seed(2)
problem = RandomGridSearchProblem(6, 8, blocks=blocks, use_heuristic=False)
problem.print_grid()
path, totalCost, numStatesExplored = ucs.solve(problem)

problem.use_heuristic = True
path, totalCostWithHeuristic, numStatesExplored = ucs.solve(problem)
originalTotalCost = totalCostWithHeuristic = problem.heuristic((0, 0))
print('Original total cost = {}'.format(totalCost))
