import util

ll = util.LinkedList.create_list(5, 4, 3, 2, 1)
print(ll)
print(ll.car())

ll2 = ll.cons(6)                # construct new list with a value 6
print(ll2)

ll3 = ll.cdr()                  # extract sub-list that don't contain the head
print(ll3)

ll4 = ll3.cons(7)
print(ll4)

print(ll.cdr() is ll4.cdr() is ll2.cdr().cdr())  # linked lists share the sub-list
