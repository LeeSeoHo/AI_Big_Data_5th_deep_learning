import random

#================================================
# Constaints
#================================================

FIRST_PLAYER = 'X'
SECOND_PLAYER = 'O'
EMPTY = ''
INT_INF = 100000000000000
WIN_REWARD  = +100000

WIN_CONDITIONS = [
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9),
    (1, 5, 9),
    (3, 5, 7),
]

#================================================
# Global variables
#================================================

MIN_PLAYER = None
NAX_PLAYER = None

#================================================
# Game functions
#================================================

def draw_board(state):
    print('')
    for row in range(3):
        for col in range(3):
            idx = 3*row + col+1
            value = state[idx]
            if value != EMPTY:
                print(value, end=' ')
            else:
                print(idx, end=' ')
        print('')
    print('')
    
def get_board_str(state):
    result = 'PLAYER:'+state['player']
    for i in range(1, 10):
        if state[i] != '':
            result += ' %d:%s'%(i,state[i])
    return result
    
def is_win(state):
    player = get_player_from_state(state)
    for condition in WIN_CONDITIONS:
        if player == state[condition[0]] == state[condition[1]] == state[condition[2]]:
            return True
    return False
        
def is_lose(state):
    player = get_player_from_state(state)
    player = get_next_player(player)
    for condition in WIN_CONDITIONS:
        if player == state[condition[0]] == state[condition[1]] == state[condition[2]]:
            return True
    return False
    
def is_draw(state):
    return sum(state[idx] == EMPTY for idx in range(1, 10)) == 0
        
def is_end(state):
    # Win or loss
    for condition in WIN_CONDITIONS:
        if (state[condition[0]] == state[condition[1]] == state[condition[2]]) and (state[condition[0]] in [MAX_PLAYER, MIN_PLAYER]):
            return True
            
    # Draw
    if sum(state[idx] == EMPTY for idx in range(1, 10)) == 0:
        return True
        
    return False
    
def utility(state):
    for condition in WIN_CONDITIONS:
        if state[condition[0]] == state[condition[1]] == state[condition[2]]:
            if state[condition[0]] == MAX_PLAYER:
                return WIN_REWARD
            else:
                return -WIN_REWARD
    
    return 0
  
def choose_starter(is_random=False):
    if is_random:
        if random.randint(0, 1) == 0:
            return FIRST_PLAYER, SECOND_PLAYER
        else:
            return SECOND_PLAYER, FIRST_PLAYER
    else:
        while True:
            print('Do you want to be the first player? (y/n):', end=' ')
            answer = input()
            if answer == 'y':
                return FIRST_PLAYER, SECOND_PLAYER
            elif answer == 'n':
                return SECOND_PLAYER, FIRST_PLAYER
        
def get_initial_state():
    state = {i: EMPTY for i in range(1, 10)}
    state['player'] = FIRST_PLAYER
    return state
        
def get_next_state(state, action):
    assert state[action] == EMPTY
    import copy
    new_state = copy.deepcopy(state)
    new_state[action] = state['player']
    new_state['player'] = get_next_player(state['player'])
    return new_state
    
def get_next_player(player):
    if player == FIRST_PLAYER:
        return SECOND_PLAYER
    else:
        return FIRST_PLAYER
        
def get_possible_actions(state):
    possible_actions = []
    for row in range(3):
        for col in range(3):
            idx = 3*row + col+1
            if state[idx] == EMPTY:
                possible_actions.append(idx)
    assert len(possible_actions) > 0
    return possible_actions
    
def get_player_from_state(state):
    return state['player']
    
