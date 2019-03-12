
#================================================
# Constaints
#================================================

INT_INF = 100000000000000
MAX_PLAYER = 'MAX'
MIN_PLAYER = 'MIN'

#================================================
# Game functions
#================================================
        
def is_end(state):
    if state[0] == MAX_PLAYER and state[1] in ['E', 'F', 'G', 'H', 'I', 'J']:
        return True
    else:
        return 
        
def utility(state):
    if state[1] == 'E':     return -50
    elif state[1] == 'F':   return  50
    elif state[1] == 'G':   return   1
    elif state[1] == 'H':   return   3
    elif state[1] == 'I':   return  -5
    elif state[1] == 'J':   return  15
    else:                   return   0
    
def get_initial_state():
    return (MAX_PLAYER, 'A')
        
def get_next_state(state, action):
    if state[0] == MAX_PLAYER:
        if state[1] == 'A':
            if action == 'a1':      return (MIN_PLAYER, 'B')
            elif action == 'a2':    return (MIN_PLAYER, 'C')
            elif action == 'a3':    return (MIN_PLAYER, 'D')
    else:
        if state[1] == 'B':
            if action == 'b1':      return (MAX_PLAYER, 'E')
            elif action == 'b2':    return (MAX_PLAYER, 'F')
        elif state[1] == 'C':
            if action == 'c1':      return (MAX_PLAYER, 'G')
            elif action == 'c2':    return (MAX_PLAYER, 'H')
        elif state[1] == 'D':
            if action == 'd1':      return (MAX_PLAYER, 'I')
            elif action == 'd2':    return (MAX_PLAYER, 'J')
    return (None, None)
    
def get_next_player(player):
    if player == MAX_PLAYER:
        return MIN_PLAYER
    else:
        return MAX_PLAYER
        
def get_possible_actions(state):
    if state[0] == MAX_PLAYER:
        if state[1] == 'A':     return ['a1', 'a2', 'a3']
        else:                   return []
    else:
        if state[1] == 'B':     return ['b1', 'b2']
        elif state[1] == 'C':   return ['c1', 'c2']
        elif state[1] == 'D':   return ['d1', 'd2']
        else:                   return []
        
def get_player_from_state(state):
    return state[0]