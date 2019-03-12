import game
import ai
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Agent type is not specified!')
    agent_type = sys.argv[1]
    
    if agent_type == 'minimax':
        agent = ai.MinimaxAgent()
    elif agent_type == 'expectimax':
        agent = ai.ExpectimaxAgent()
    elif agent_type == 'pruning':
        agent = ai.PruningMinimaxAgent()
    else:
        raise Exception('Undefined agent type! (%s)'%agent_type)
    
    print('-'*40)
    initial_state = game.get_initial_state()
    print('state =', initial_state)
    print('value =', agent.V(initial_state))
    print('policy =', agent.policy(initial_state))
    
    print('-'*40)
    another_state = (game.MIN_PLAYER, 'B')
    print('state =', another_state)
    print('value =', agent.V(another_state))
    print('policy =', agent.policy(another_state))

