import util

pq = util.PriorityQueue()

print(pq.update('A', 10))
print(pq.update('B', 20))
print(pq.update('C', 30))
print(pq.update('A', 5))

print(pq.heap[0])
print(pq.remove_min())