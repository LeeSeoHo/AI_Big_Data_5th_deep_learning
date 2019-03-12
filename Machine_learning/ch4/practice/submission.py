import util, math, random
from collections import defaultdict
from util import ValueIteration

############################################################
# Problem A

class ExampleMDP(util.MDP):
    def startState(self):
        return 0

    # Return set of actions possible from |state|.
    def actions(self, state):
        return ['Left', 'Right']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        if state == -2 or state == 2:
            return []
        
        leftReward = -5
        rightReward = -5

        if state - 1 == -2:
            leftReward = 20
        if state + 1 == 2:
            rightReward = 100
        
        if action == 'Left':
            results = [(state-1, 0.8, leftReward), (state+1, 0.2, rightReward)]
        elif  action == 'Right':
            results = [(state-1, 0.7, leftReward), (state+1, 0.3, rightReward)]
        else:
            results = []
        
        return results
            
    def discount(self):
        return 1


############################################################
# Problem C

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.
    # The second element is the index (not the value) of the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.
    # The final element is the current deck.
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None. 
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE
        succ_prob_reward_list = []
        card_sum, peek_idx, deck = state  # card_sum = the sum of taken cards' values

        if deck is None:  # when there is no card in the deck
            pass          # no possible successor state

        elif action == 'Take':
            num_all_cards = sum(deck)  # the number of all cards

            # get_succ_reward(idx) returns a successor state and a reward, when a card is taken.
            def get_succ_reward(idx):
                new_card_sum = card_sum + self.cardValues[idx]  # what's the new sum of card values, when we take a new card?
                if new_card_sum > self.threshold:  # when the card sum exceeds the threshold
                    new_deck = None
                    reward = 0
                elif num_all_cards > 1:  # sum(new_deck) > 0; when some cards remain
                    new_deck = _X_       # it may need multiple lines
                    reward = 0
                else:  # when there is no card remaining
                    new_deck = None
                    reward = new_card_sum
                succ = new_card_sum, None, new_deck
                return succ, reward

            # Peek implementation ----------------------------------------
            if peek_idx is not None:  # when previous action was 'Peek'
                succ, reward = get_succ_reward(peek_idx)
                succ_prob_reward_list.append((succ, _X_, reward))
            # ---------------------------------------- Peek implementation
            else:  # when previous action was not 'Peek'
                for idx, num in enumerate(deck):
                    if num == 0:
                        continue                        
                    succ, reward = get_succ_reward(idx)
                    prob = _X_
                    succ_prob_reward_list.append((succ, prob, reward))

        # Peek implementation ----------------------------------------
        elif action == 'Peek':
            if peek_idx is None:
                num_all_cards = sum(deck)

                for idx, num in enumerate(deck):
                    if num == 0:
                        continue
                    prob = _X_
                    succ_prob_reward_list.append(((card_sum, idx, deck), prob, - self.peekCost))
        # ---------------------------------------- Peek implementation

        elif action == 'Quit':
            succ_prob_reward_list.append(((card_sum, None, None), 1, card_sum))

        else:
            raise ValueError("Undefined action '{}'".format(action))

        return succ_prob_reward_list
        # END_YOUR_CODE

    def discount(self):
        return 1


############################################################

# Problem D: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE
        if newState is None:
            v_opt = 0
        else:
            v_opt = max(self.getQ(newState, a) for a in self.actions(newState))  # v_opt(s')
        diff = self.getQ(state, action) - (reward + self.discount * v_opt)
        for f, v in self.featureExtractor(state, action):
            eta = self.getStepSize()
            self.weights[f] -= _X_
        # END_YOUR_CODE

# Return a singleton list containing indicator feature for the (state, action)
# pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]


############################################################

# Problem E: convergence of Q-learning

def compareQLandVI(targetMDP, featureExtractor):
    QL = QLearningAlgorithm(targetMDP.actions, 1, featureExtractor)
    VI = ValueIteration()
    
    util.simulate(targetMDP, QL, numTrials=30000)
    VI.solve(targetMDP)

    diffPolicyStates = []
    QL.explorationProb = 0
    for state in targetMDP.states:
        #print state, QL.getAction(state), VI.pi[state]
        if QL.getAction(state) != VI.pi[state]:
            diffPolicyStates.append(state)
    print("%d/%d = %f%% different states"%(len(diffPolicyStates), len(targetMDP.states), len(diffPolicyStates)/float(len(targetMDP.states))))


############################################################

# Problem F: features for Q-learning.

# You should return a list of (feature key, feature value) pairs (see
# identityFeatureExtractor()).
# Implement the following features:
# - indicator on the total and the action (1 feature).
# - indicator on the presence/absence of each card and the action (1 feature).
#       Example: if the deck is (3, 4, 0 , 2), then your indicator on the presence of each card is (1,1,0,1)
#       Only add this feature if the deck != None
# - indicator on the number of cards for each card type and the action (len(counts) features).  Only add these features if the deck != None
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state
    # BEGIN_YOUR_CODE
    type_1, type_2, type_3 = list(range(3))  # we have 3 types of features
    features = []

    # type 1
    features.append((type_1, (total, action)))

    if counts != None:
        # type 2
        features.append((type_2, (tuple(1 if count > 0 else 0 for count in counts), action)))

        for idx, num in enumerate(counts):
            # type 3
            features.append((type_3, (idx, num, action)))

    # all features have 1s as values
    return [(feature, 1) for feature in features]
    # END_YOUR_CODE


############################################################

