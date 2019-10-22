import math
import copy
from collections import deque
import heapq
from itertools import product, permutations


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
  
class SearchProblem:
  def __init__(self, goal, model, auxheur = []):
    self.goal = goal
    self.model = model
    # self.auxheur = auxheur

    self.mindepth = {}
    self.calculateNumTrips(self.goal)

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
      if anyorder:
          possibleGoals = list(permutations(self.goal))
          bestScore = math.inf
          for g in possibleGoals:
              s = self.f(0, init, g)
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
      heapq.heappush(heap, (self.f(searchTree[root]['stepCount'], init, self.goal), root))

      numExpansion = 0
      while(len(heap) > 0):
          numExpansion += 1

          curr = heapq.heappop(heap)[1]
          if curr == tuple(self.goal):
              return self.traceback(searchTree)
          
          if numExpansion > limitexp or searchTree[curr]['stepCount'] > limitdepth:
              continue 

          # Generate possible moves
          possibleMoves = list(product(*[tuple(tuple(move) for move in self.model[pos] if searchTree[curr]['tickets'][move[0]] > 0) for pos in curr]))

          # Add valid moves (restrictions below)
          #     1: 2 agents can't be in the same place at the same time
          #     2: Limited tickets
          #     3: Do not add existing states - If it already exists, 
          #         it's the closest one
          for move in possibleMoves:
              # destVertices = tuple([action[1] for action in move])
              # typeTransport = [action[0] for action in move]
              typeTransport, destVertices = zip(*move) # also makes a big difference in time

              #  restriction 3                 restriction 1
              if destVertices in searchTree or len(set(destVertices)) != len(move):
                  continue

              # newTickets = copy.deepcopy(searchTree[curr]['tickets'])
              newTickets = [*searchTree[curr]['tickets']] # This makes so much difference!!
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

              heapq.heappush(heap, (self.f(searchTree[destVertices]['stepCount'], destVertices, self.goal), destVertices))

      print("No path found")
      return

  def traceback(self, searchTree):
      res = deque()
      appendleft = res.appendleft
      curr = tuple(self.goal)
      while curr != False:
          appendleft((searchTree[curr]['typeTransport'], list(curr)))
          curr = searchTree[curr]['parent']
      return res
      

  def calculateNumTrips(self, goalList):
      for goal in goalList:
          q = deque([goal])
          self.mindepth[(goal, goal)] = 0
          while(len(q) > 0): # BFS to find minimum depth
              curr = q.popleft()
              for adj in self.model[curr]:
                  vert = adj[1]
                  if (vert, goal) in self.mindepth: # already visited
                      continue

                  self.mindepth[(vert, goal)] = self.mindepth[(curr, goal)] + 1
                  q.append(vert)

  # Our heuristic function
  # best case scenario: it will get to the goal
  # in the greatest minimum steps value
  def f(self, cost, vertices, goals):
      return max([cost + self.mindepth[(vertices[i], goals[i])] for i in range(len(vertices))])

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
