import game
import ai
import sys

agent = None

def user_turn(state):
    game.draw_board(state)
    
    while True:
        print('What is your next move? (1-9):', end=' ')
        action = int(input())
        if state[action] == game.EMPTY:
            break
    
    state = game.get_next_state(state, action)
    
    if game.is_win(state):
        game.draw_board(state)
        print('Lose!')
        return None
        
    if game.is_lose(state):
        game.draw_board(state)
        print('Win!')
        return None
    
    if game.is_draw(state):
        game.draw_board(state)
        print('Draw!')
        return None

    return state
    
def system_turn(state):
    action = agent.policy(state)
    print('action =', action)
    
    state = game.get_next_state(state, action)
    
    if game.is_win(state):
        game.draw_board(state)
        print('Win!')
        return None
    
    if game.is_lose(state):
        game.draw_board(state)
        print('Lose!')
        return None
        
    if game.is_draw(state):
        game.draw_board(state)
        print('Draw!')
        return None
     
    return state
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Agent type is not specified!')
    agent_type = sys.argv[1]
    
    if agent_type == 'minimax':
        agent = ai.MinimaxAgent()
    elif agent_type == 'pruning':
        agent = ai.PruningMinimaxAgent()
    elif agent_type == 'limited':
        if len(sys.argv) < 3:
            raise Exception('Depth is not specified!')
        depth = int(sys.argv[2])
        agent = ai.DepthLimitedMinimaxAgent(depth)
    else:
        raise Exception('Undefined agent type! (%s)'%agent_type)
        
    game.MIN_PLAYER, game.MAX_PLAYER = game.choose_starter()
    print('You: %s, Computer; %s'%(game.MIN_PLAYER, game.MAX_PLAYER))
    
    state = game.get_initial_state()
    
    if game.FIRST_PLAYER == game.MIN_PLAYER:
        fist_player = user_turn
        second_player = system_turn
    else:
        fist_player = system_turn
        second_player = user_turn
    
    while True:
        state = fist_player(state)
        if state is None:
            break
        
        state = second_player(state)
        if state is None:
            break