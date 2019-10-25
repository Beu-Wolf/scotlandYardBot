# Grupo 007 - Afonso Gonçalves 89399, Daniel Seara 89427

import math
import copy
from collections import deque
import heapq
from itertools import product, permutations


# Advanced
#   1: Use deque instead of list:       https://stackoverflow.com/questions/23487307/python-deque-vs-list-performance-comparison
#   2: Use deque instead of queue:      https://stackoverflow.com/questions/717148/queue-queue-vs-collections-deque
#   3: Comprehension lists:             https://www.pythonforbeginners.com/basics/list-comprehensions-in-python
#   4: lambda function scoping:         https://louisabraham.github.io/articles/python-lambda-closures.html
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
  
class Node:
    def __init__(self, f, node):
        self.f = f
        self.node = node

    def __lt__(self, other):
        return self.f < other.f or self.node['g'] < other.node['g']

    def __repr__(self):
        res = "\n{ score: " + str(self.f)
        for k in self.node:
            res+= "\n" + str(k) + ": " + str(self.node[k])

        return res + "}"

class SearchProblem:
  def __init__(self, goal, model, auxheur = []):
    self.goal = goal
    self.model = model

    self.mindepth = {}
    self.calculateNumTrips(self.goal)

  # Our heuristic function
  # best case scenario: it will get to the goal
  #  in the greatest minimum steps values
  def f(self, cost, vertices, goals):
      return max([cost + 2*self.mindepth[(vertices[i], goals[i])] for i in range(len(vertices))])

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
      if anyorder:
          possibleGoals = list(permutations(self.goal))
          bestScore = math.inf
          for g in possibleGoals:
              s = self.f(0, init, g)
              if s < bestScore:
                  bestScore = s
                  self.goal = g

      root = {
        'vertices': init,
        'parent': False,
        'typeTransport': [],
        'tickets': tickets,
        'g': 0
      }

      # min-heap of nodes, sorted by self.f(g, vertex, goal) value
      heap = []
      heapq.heappush(heap, Node(self.f(root['g'], root['vertices'], self.goal), root))

      numExpansions = 0
      while(len(heap) > 0):
          numExpansions+=1
          curr = heapq.heappop(heap).node

          # Check if goal
          if curr['vertices'] == tuple(self.goal):
              return self.traceback(curr)
          
          # Check limit expansions/depth
          if numExpansions > limitexp or curr['g'] > limitdepth:
              print("Limit exceeded")
              continue
    
          # Generate possible moves
          possibleMoves = list(product(*[tuple(tuple(move) for move in self.model[pos] if curr['tickets'][move[0]] > 0) for pos in curr['vertices']]))

          # Add valid moves (restrictions below)
          #     1: Limited tickets
          #     2: 2 agents can't be in the same place at the same time
          for move in possibleMoves:
              typeTransport, destVertices = zip(*move)

              # Get new tickets
              newTickets = [*curr['tickets']]
              for t in typeTransport:
                  newTickets[t]-=1

              # Restricion #1
              if [a for a in newTickets if a < 0]:
                  # print("No tickets!")
                  continue
              
              # Restriction #2
              if len(set(destVertices)) != len(move):
                  # print("Invalid position")
                  continue

              node = {
                'vertices': destVertices,
                'parent': curr,
                'typeTransport': typeTransport,
                'tickets': newTickets,
                'g': curr['g'] + 1
              }

              # add to heap
              heapq.heappush(heap, Node(self.f(node['g'], destVertices, self.goal), node))
      print("No path found")
      return

  def traceback(self, goalNode):
      res = deque()
      appendleft = res.appendleft
      curr = goalNode
      while curr:
          appendleft([list(curr['typeTransport']), list(curr['vertices'])])
          curr = curr['parent']

      return list(res)


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
