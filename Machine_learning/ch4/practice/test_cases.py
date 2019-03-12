
from submission import *
from util import *


def main():
    try:
        print('\n========== Problem A ==========')
        mdp = ExampleMDP()
        algorithm = ValueIteration()
        algorithm.solve(mdp, 20, verbose=True) # when epsilon=20, the algorithm repeats 2 iterations
        for i in [-2, -1, 0, 1, 2]:
            print("Value of the state '%d' : %f"%(i, algorithm.V[i]))

        for i in [-1, 0, 1]:
            print("Plicy at the state '%d' : %s"%(i, algorithm.pi[i]))

        print('\n========== Problem C ==========')
        mdp1 = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)
        startState = mdp1.startState()
        preBustState = (6, None, (1, 1))
        postBustState = (11, None, None)

        mdp2 = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)
        preEmptyState = (11, None, (1,0))

        print('\n---------- Test c1 ----------')
        # Make sure the succAndProbReward function is implemented correctly.

        vanilla_tests = [
            ([((1, None, (1, 2)), 0.5, 0), ((5, None, (2, 1)), 0.5, 0)], mdp1, startState, 'Take'),
            ([((0, None, None), 1, 0)], mdp1, startState, 'Quit'),
            ([((7, None, (0, 1)), 0.5, 0), ((11, None, None), 0.5, 0)], mdp1, preBustState, 'Take'),
            ([], mdp1, postBustState, 'Take'),
            ([], mdp1, postBustState, 'Quit'),
            ([((12, None, None), 1., 12)], mdp2, preEmptyState, 'Take'),
        ]

        print('Vanilla Blackjack')
        for no, (answer, mdp, state, action) in enumerate(vanilla_tests):
            print('No %d'%(no+1), end=' ')
            if answer != mdp.succAndProbReward(state, action):
                print('=> wrong')
            else:
                print('=> right')
            print('- state: {}, action: {}'.format(state, action))
            print('- true answer =', answer)
            print('- your answer =', mdp.succAndProbReward(state, action))

        print('\n---------- Test c2 ----------')
        peek_tests = [
            ([((0, 0, (2, 2)), 0.5, -1), ((0, 1, (2, 2)), 0.5, -1)], mdp1, startState, 'Peek'),
            ([((1 , None, (1, 2) ), 1, 0)] , mdp1, (0, 0, (2, 2)), 'Take'),
            ([], mdp1, postBustState, 'Peek'),
            ]

        print('Peeking Blackjack')
        for no, (answer, mdp, state, action) in enumerate(peek_tests):
            print('No %d'%(no+1), end=' ')
            if answer != mdp.succAndProbReward(state, action):
                print('=> wrong')
            else:
                print('=> right')
            print('- state: {}, action: {}'.format(state, action))
            print('- true answer =', answer)
            print('- your answer = ', mdp.succAndProbReward(state, action))

        print('\n---------- Test c3 ----------')
        algorithm = ValueIteration()
        algorithm.solve(mdp1, verbose=True)
        for s in algorithm.V:
            print('V(%s) = %f'%(s, algorithm.V[s]))
        print('------------')
        for s in algorithm.pi:
            print('pi(%s) = %s'%(s, algorithm.pi[s]))
        print('------------')
        print('Q1 (6, None, (1, 1) => %s'%(algorithm.pi[(6, None, (1, 1))]))
        print('Q2 (6, 0, (1, 1) => %s'%(algorithm.pi[(6, 0, (1, 1))]))

        print('\n========== Problem D ==========')
        mdp = util.NumberLineMDP()
        rl = QLearningAlgorithm(mdp.actions, mdp.discount(), identityFeatureExtractor, 0)

        # We call this here so that the stepSize will be 1
        rl.numIters = 1

        rl.incorporateFeedback(0, 1, 0, 1)
        print('Q-value for (state = 0, action = -1) : Answer %.1f, Output %.1f'%(0, rl.getQ(0, -1)))
        print('Q-value for (state = 0, action =  1) : Answer %.1f, Output %.1f'%(0, rl.getQ(0, 1)))

        rl.incorporateFeedback(1, 1, 1, 2)
        print('Q-value for (state = 0, action = -1) : Answer %.1f, Output %.1f'%(0, rl.getQ(0, -1)))
        print('Q-value for (state = 0, action =  1) : Answer %.1f, Output %.1f'%(0, rl.getQ(0, 1)))
        print('Q-value for (state = 1, action = -1) : Answer %.1f, Output %.1f'%(0, rl.getQ(1, -1)))
        print('Q-value for (state = 1, action =  1) : Answer %.1f, Output %.1f'%(1, rl.getQ(1, 1)))

        rl.incorporateFeedback(2, -1, 1, 1)
        print('Q-value for (state = 2, action = -1) : Answer %.1f, Output %.1f'%(1.9, rl.getQ(2, -1)))
        print('Q-value for (state = 2, action =  1) : Answer %.1f, Output %.1f'%(0, rl.getQ(2, 1)))

        print('\n========== Problem E ==========')
        # Small test case
        smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)
        compareQLandVI(smallMDP, identityFeatureExtractor)

        # Large test case
        largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)
        compareQLandVI(largeMDP, identityFeatureExtractor)
        print('\n========== Problem F ==========')

        mdp = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)
        rl = QLearningAlgorithm(mdp.actions, mdp.discount(), blackjackFeatureExtractor, 0)

        # We call this here so that the stepSize will be 1
        rl.numIters = 1

        rl.incorporateFeedback((7, None, (0, 1)), 'Quit', 7, (7, None, None))
        print("Q-value for (state = (7, None, (0, 1)), action = 'Quit') : Answer %.1f, Output %.1f"%(28, rl.getQ((7, None, (0, 1)), 'Quit')))
        print("Q-value for (state = (7, None, (1, 0)), action = 'Quit') : Answer %.1f, Output %.1f"%(7, rl.getQ((7, None, (1, 0)), 'Quit')))
        print("Q-value for (state = (2, None, (0, 2)), action = 'Quit') : Answer %.1f, Output %.1f"%(14, rl.getQ((2, None, (0, 2)), 'Quit')))
        print("Q-value for (state = (2, None, (0, 2)), action = 'Take') : Answer %.1f, Output %.1f"%(0, rl.getQ((2, None, (0, 2)), 'Take')))

        # Large test case
        largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)
        compareQLandVI(largeMDP, blackjackFeatureExtractor)

    except NotImplementedError as err:
        # print err
        print("\nNotImplementedError: you didn't implement the function.")


if __name__ == '__main__':
    main()
