import math
import copy
from collections import deque
import heapq
import itertools


# Advanced
#   1: Use deque instead of list:       https://stackoverflow.com/questions/23487307/python-deque-vs-list-performance-comparison
#   2: Use deque instead of queue:      https://stackoverflow.com/questions/717148/queue-queue-vs-collections-deque
#   3: Comprehension lists:             https://www.pythonforbeginners.com/basics/list-comprehensions-in-python
#   4: DON'T use lists as dict keys:    https://wiki.python.org/moin/DictionaryKeys
#   5: lambda function scoping:         https://louisabraham.github.io/articles/python-lambda-closures.html
#
# Complexity classes
#   https://www.ics.uci.edu/~brgallar/week8_2.html
#   https://wiki.python.org/moin/TimeComplexity
#
# Documentation:
#   deque: https://docs.python.org/3.7/library/collections.html#collections.deque
#   itertools: https://docs.python.org/3.7/library/itertools.html
#
# Heuristics
#   https://cs.stackexchange.com/questions/37043/given-two-heuristic-values-how-do-i-tell-which-one-is-admissible
#
# Questions:
#   Use global variables so we don't have to pass the object to functions?
#   Does heuristic funcion have to receive the goal? It's the same for every problem
#
# TODOS:
#   Change heuristic function name (score seems like a good thing, but we are trying to minimize it
#       Suggestions:
#           * f (use bibliograpy notation)
#           * h
#           * estimatedCost
#           * heuristic
  
class SearchProblem:
  def __init__(self, goal, model, auxheur = []):
    self.goal = goal
    self.model = model
    # self.auxheur = auxheur

    self.mindepth = {}
    self.calculateNumTrips(self.goal)

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
      if anyorder:
          possibleGoals = list(itertools.permutations(self.goal))
          bestScore = math.inf
          for g in possibleGoals:
              s = self.score(0, init, g)
              if s < bestScore:
                  bestScore = s
                  self.goal = g
 

      root = tuple(init)
      searchTree = {}
      searchTree[root] = {
          'parent': False,
          'typeTransport': [],
          'tickets': tickets,
          'stepCount': 0
      }

      # heap is a heap of tuples (heuristic, (position)) so we can compare combinations by their heuristic
      # position is a tuple so we can use it as a dict key (see Advanced#4)
      heap = []
      heapq.heappush(heap, (self.score(searchTree[root]['stepCount'], init, self.goal), root))
      # print(heap)
      # print(searchTree)

      numExpansion = 0
      while(len(heap) > 0):
          numExpansion += 1

          curr = heapq.heappop(heap)[1]
          # print("===================Popped", curr)
          if curr == tuple(self.goal):
              return self.traceback(searchTree)
          
          if numExpansion > limitexp or searchTree[curr]['stepCount'] > limitdepth:
              continue 
          

          # Generate possible moves
          possibleMoves = [tuple(tuple(move) for move in self.model[pos] if searchTree[curr]['tickets'][move[0]] > 0) for pos in curr]

          
          # print("List of moves per agent:", possibleMoves)
          possibleMoves = list(itertools.product(*possibleMoves))
          # print("List of all combinations:", possibleMoves)   

          # Add valid moves
          # Move restrictions
          #     1: 2 agents can't be in the same place at the same time
          #     2: Limited tickets
          #     3: (?) Do not add existing states. If it already exists, 
          #         it's the closest one TODO: check this
          #     4: If move equals to goal, add to heap and break. It will be removed in the next iteration
          #         We should check if popped move from heap equals goal when popping...
          validMoves = []
          for move in possibleMoves:
              destVertices = tuple(action[1] for action in move)
              typeTransport = [action[0] for action in move]
              if destVertices in searchTree:
                  continue
              
              if len(set(destVertices)) != len(move): # check rule#1
                  continue

              newTickets = copy.deepcopy(searchTree[curr]['tickets'])
              for t in typeTransport:
                  newTickets[t] -= 1
              if len([a for a in newTickets if a < 0]) > 0:
                  continue
                  
              
              searchTree[destVertices] = {
                  'parent': curr,
                  'typeTransport': typeTransport,
                  'tickets': newTickets,
                  'stepCount': searchTree[curr]['stepCount'] + 1
              }

              

              heapq.heappush(heap, (self.score(searchTree[destVertices]['stepCount'], destVertices, self.goal), destVertices))
              validMoves.append(move)

          # print("Valid moves:", validMoves)   

      return

  def traceback(self, searchTree):
      res = deque()
      curr = tuple(self.goal)
      while curr != False:
          res.appendleft((searchTree[curr]['typeTransport'], list(curr)))
          curr = searchTree[curr]['parent']
      return res
      # return list(res)
      

  def calculateNumTrips(self, goalList):
      for goal in goalList:
          q = deque([goal])
          # inQueue = [False] * len(self.model)
          # inQueue[goal] = True
          # print(len(inQueue))
          self.mindepth[(goal, goal)] = 0
          # TODO: if this value was previously set,
          # we don't have to calculate again for every vertex
          #     WARNING: we calculate costs for goal 61 twice!!!
          while(len(q) > 0): # BFS to find minimum depth
              curr = q.popleft()
             

              # discuss: check if visited by checking if key exists
              #     or keep inQueue? __ vs O(1)
              for adj in self.model[curr]:
                  vert = adj[1]
                  if (vert, goal) in self.mindepth: # already visited
                      continue

                  self.mindepth[(vert, goal)] = self.mindepth[(curr, goal)] + 1
                  q.append(vert)

  # Our heuristic function
  # best case scenario: it will get to the goal
  # in the greatest minimum steps value
  def score(self, cost, vertices, goals):
      return max([cost + self.mindepth[(vertices[i], goals[i])] for i in range(len(vertices))])

  # SAME AS: TODO: delete this comment
  #     ret = 0
  #     for i in range(len(cost)):
  #         ret = max([ret, auxcosts[i] + self.mindepth[(vertices[i], goals[i])]])
  #     return ret

# =============================================== END OF CLASS ============================================

# TODO: Remove <3
def printStatus(status):
  for i in status.keys():
    print(i, status[i])


def calcDist(auxheur, point, objective):
  x = auxheur[objective][0] - auxheur[point][0]
  y = auxheur[objective][1] - auxheur[point][1]

  return math.sqrt(x**2 + y**2)

def printDict(d):
    for k in d:
        print(k, d[k])
