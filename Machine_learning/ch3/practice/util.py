import collections
import heapq
from functools import reduce

############################################################
# Abstract interfaces for search problems and search algorithms.

class SearchProblem:
    # Return the start state.
    def start_state(self): raise NotImplementedError("Override me")

    # Return whether |state| is an end state or not.
    def is_end(self, state): raise NotImplementedError("Override me")

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    def succ_and_cost(self, state): raise NotImplementedError("Override me")

class SearchAlgorithm:
    # First, call solve on the desired SearchProblem |problem|.
    # Then it should set two things:
    # - self.actions: list of actions that takes one from the start state to an end
    #                 state; if no action sequence exists, set it to None.
    # - self.totalCost: the sum of the costs along the path or None if no valid
    #                   action sequence exists.
    def solve(self, problem): raise NotImplementedError("Override me")

# Data structure for supporting uniform cost search.
class PriorityQueue:
    def  __init__(self):
        self.heap = []
        self.heap_node_dict = {}

    # Insert |item| into the heap with priority |newPriority|.
    # Return whether the priority queue was updated.
    def update(self, item, new_priority):
        old_heap_node = self.heap_node_dict.get(item)

        # set removal flag of the old item
        if old_heap_node:       # when old_heap_node exists (when it's not None)
            if new_priority < old_heap_node[0]:
                old_heap_node[2] = True  # set removal_flag

        # add the new item
        if not old_heap_node or new_priority < old_heap_node[0]:
            # heap_node --> [priority, item, removal_flag]
            new_heap_node = [new_priority, item, False]
            heapq.heappush(self.heap, new_heap_node)
            self.heap_node_dict[item] = new_heap_node
            return True
        else:
            return False

    # Returns (item with minimum priority, priority)
    # or (None, None) if the priority queue is empty.
    def remove_min(self):
        removal_flag = True
        while removal_flag:
            priority, item, removal_flag = heapq.heappop(self.heap)
            self.heap_node_dict.pop(item, None)  # https://stackoverflow.com/a/15411146
        return (item, priority)

    def is_empty(self):
        while len(self.heap) > 0 and self.heap[0][2]:
            priority, item, removal_flag = heapq.heappop(self.heap)
            self.heap_node_dict.pop(item, None)
        return len(self.heap) == 0


class LinkedList(tuple):
    @classmethod
    def create_list(cls, *args):
        return reduce(lambda lst, el: cls((el, lst)), reversed(args), LinkedList.NIL)

    def cons(self, el):
        return LinkedList((el, self))

    def car(self):
        return self[0] if self is not LinkedList.NIL else self

    def cdr(self):
        return self[1] if self is not LinkedList.NIL else self

    def nth(self, n):
        lst = self
        while n > 0:
            n -= 1
            lst = self.cdr()
        return lst.car()

    def __len__(self):
        lst = self
        count = 0
        while lst is not LinkedList.NIL:
            count += 1
            lst = lst.cdr()
        return count

    def __iter__(self):
        lst = self
        while lst is not LinkedList.NIL:
            yield lst.car()
            lst = lst.cdr()

    def __reversed__(self):
        items = tuple(self)
        for item in reversed(items):
            yield item

    def __repr__(self):
        return str(tuple(self))

    def find(self, value, key=lambda x: x):
        lst = self
        while lst is not LinkedList.NIL:
            if key(lst.car()) == value:
                return lst
            lst = lst.cdr()
        return lst


class NilList(LinkedList):
    def __repr__(self):
        return 'NIL'


LinkedList.NIL = NilList()
