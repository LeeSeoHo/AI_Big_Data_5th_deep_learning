#!/usr/bin/env python

import graderUtil

grader = graderUtil.Grader()
submission = grader.load('submission')

FINAL_GRADE = True
SEED = 'testing' # random seed at the beginning of each question for more fairness in grading...                              
BIG_NEGATIVE = -10000

from game import Agent
from ghostAgents import RandomGhost, DirectionalGhost
import random, math, traceback, sys, os

import pacman, time, layout, textDisplay
textDisplay.SLEEP_TIME = 0
textDisplay.DRAW_EVERY = 1000
thismodule = sys.modules[__name__]


grader.addBasicPart('writeupValid', lambda : grader.requireIsValidPdf('pacman.pdf'), 0)

def run(layname, pac, ghosts, nGames = 1, name = 'games'):
  """
  Runs a few games and outputs their statistics.
  """
  if grader.fatalError:
    return {'time': 65536, 'wins': 0, 'games': None, 'scores': [0]*nGames, 'timeouts': nGames}

  starttime = time.time()
  lay = layout.getLayout(layname, 3)
  disp = textDisplay.NullGraphics()

  print('*** Running %s on' % name, layname,'%d time(s).' % nGames)
  games = pacman.runGames(lay, pac, ghosts, disp, nGames, False, catchExceptions=False)
  print('*** Finished running %s on' % name, layname,'after %d seconds.' % (time.time() - starttime))
  
  stats = {'time': time.time() - starttime, 'wins': [g.state.isWin() for g in games].count(True), 'games': games, 'scores': [g.state.getScore() for g in games], 'timeouts': [g.agentTimeout for g in games].count(True)}
  print('*** Won %d out of %d games. Average score: %f ***' % (stats['wins'], len(games), sum(stats['scores']) * 1.0 / len(games)))

  return stats


def comparison_checking(theirPac, ourPacOptions, agentName):
  """
  Skeleton used for question 2, 3 and 4... 
  
  Takes in their Pacman agent, wraps it in ours, and assigns points.
  """
  print('Running our grader (hidden from you)...')
  random.seed(SEED)
  offByOne = False 
  partialPlyBug = False
  totalSuboptimal = 0
  timeout = False


  return timeout, offByOne, partialPlyBug, totalSuboptimal

def test0(agentName):
  stats = {}
  if agentName == 'alphabeta':
    stats = run('smallClassic', submission.AlphaBetaAgent(depth=2), [DirectionalGhost(i + 1) for i in range(2)], name='%s (depth %d)' % ('alphabeta', 2))
  elif agentName == 'minimax':
    stats = run('smallClassic', submission.MinimaxAgent(depth=2), [DirectionalGhost(i + 1) for i in range(2)], name='%s (depth %d)' % ('minimax', 2))
  else:
    stats = run('smallClassic', submission.ExpectimaxAgent(depth=2), [DirectionalGhost(i + 1) for i in range(2)], name='%s (depth %d)' % ('expectimax', 2))
  if stats['timeouts'] > 0:
    grader.fail('Your ' + agentName + ' agent timed out on smallClassic.  No autograder feedback will be provided.')
    return
  grader.assignFullCredit()


gamePlay = {}

def test1(agentName):
  if agentName not in gamePlay and not grader.fatalError:
    if agentName == 'minimax':
      gamePlay[agentName] = comparison_checking(submission.MinimaxAgent(depth=2), {}, agentName)
    elif agentName == 'alphabeta':
      gamePlay[agentName] =  comparison_checking(submission.AlphaBetaAgent(depth=2), {agentName: 'True'}, agentName)
    elif agentName == 'expectimax':
      gamePlay[agentName] = comparison_checking(submission.ExpectimaxAgent(depth=2), {agentName: 'True'}, agentName)
    else:
      raise Exception("Unexpected agent name: " + agentName)
  
  timeout, offByOne, partialPlyBug, totalSuboptimal = gamePlay[agentName]
  if timeout:
    grader.fail('Your ' + agentName + ' agent timed out on smallClassic.  No autograder feedback will be provided.')
    return
  if offByOne: 
    grader.fail('Depth off by 1')
  grader.assignFullCredit()

def test2(agentName):
  if agentName not in gamePlay and not grader.fatalError:
    if agentName == 'minimax':
      gamePlay[agentName] = comparison_checking(submission.MinimaxAgent(depth=2), {}, agentName)
    elif agentName == 'alphabeta':
      gamePlay[agentName] =  comparison_checking(submission.AlphaBetaAgent(depth=2), {agentName: 'True'}, agentName)
    elif agentName == 'expectimax':
      gamePlay[agentName] = comparison_checking(submission.ExpectimaxAgent(depth=2), {agentName: 'True'}, agentName)
    else:
        raise Exception("Unexpected agent name: " + agentName)

  timeout, offByOne, partialPlyBug, totalSuboptimal = gamePlay[agentName]
  if timeout:
    grader.fail('Your ' + agentName + ' agent timed out on smallClassic.  No autograder feedback will be provided.')
    return
  if partialPlyBug: 
    grader.fail('Incomplete final search ply bug')
  grader.assignFullCredit()

def test3(agentName):
  if agentName not in gamePlay and not grader.fatalError:
    if agentName == 'minimax':
      gamePlay[agentName] = comparison_checking(submission.MinimaxAgent(depth=2), {}, agentName)
    elif agentName == 'alphabeta':
      gamePlay[agentName] =  comparison_checking(submission.AlphaBetaAgent(depth=2), {agentName: 'True'}, agentName)
    elif agentName == 'expectimax':
      gamePlay[agentName] = comparison_checking(submission.ExpectimaxAgent(depth=2), {agentName: 'True'}, agentName)
    else:
      raise Exception("Unexpected agent name: " + agentName)
  
  timeout, offByOne, partialPlyBug, totalSuboptimal = gamePlay[agentName]
  if timeout:
    grader.fail('Your '+agentName+' agent timed out on smallClassic.  No autograder feedback will be provided.')
    return
  if totalSuboptimal > 0: 
    grader.fail('Suboptimal moves: ' + str(totalSuboptimal))
  grader.assignFullCredit()

maxSeconds = 10
    
grader.addManualPart('1a', 5, description='Recurrence for multi-agent minimiax')
grader.addBasicPart('1b-1-basic', lambda : test0('minimax'), 4, maxSeconds=maxSeconds, description='Tests minimax for timeout on smallClassic.')
grader.addHiddenPart('1b-1-hidden', lambda : test1('minimax'), 2, maxSeconds=maxSeconds, description='Tests minimax for off by one bug on smallClassic.')
grader.addHiddenPart('1b-2-hidden', lambda : test2('minimax'), 2, maxSeconds=maxSeconds, description='Tests minimax for search depth bug on smallClassic.')
grader.addHiddenPart('1b-3-hidden', lambda : test3('minimax'), 2, maxSeconds=maxSeconds, description='Tests minimax for suboptimal moves on smallClassic.')

grader.addBasicPart('2a-0', lambda : test0('alphabeta'), 4, description='Tests alphabeta for timeout on smallClassic.')
grader.addHiddenPart('2a-1-hidden', lambda : test1('alphabeta'), 2, maxSeconds=maxSeconds, description='Tests alphabeta for off by one bug on smallClassic.')
grader.addHiddenPart('2a-2-hidden', lambda : test2('alphabeta'), 2, maxSeconds=maxSeconds, description='Tests alphabeta for search depth bug on smallClassic.')
grader.addHiddenPart('2a-3-hidden', lambda : test3('alphabeta'), 2, maxSeconds=maxSeconds, description='Tests alphabeta for suboptimal moves on smallClassic.')

grader.addManualPart('3a', 5, description='Recurrence for multi-agent expectimax')
grader.addBasicPart('3b-0-basic', lambda : test0('expectimax'), 4, maxSeconds=maxSeconds, description='Tests expectimax for timeout on smallClassic.')
grader.addHiddenPart('3b-1-hidden', lambda : test1('expectimax'), 2, maxSeconds=maxSeconds, description='Tests expectimax for off by one bug on smallClassic.')
grader.addHiddenPart('3b-2-hidden', lambda : test2('expectimax'), 2, maxSeconds=maxSeconds, description='Tests expectimax for search depth bug on smallClassic.')
grader.addHiddenPart('3b-3-hidden', lambda : test3('expectimax'), 2, maxSeconds=maxSeconds, description='Tests expectimax for suboptimal moves on smallClassic.')

grader.grade()
