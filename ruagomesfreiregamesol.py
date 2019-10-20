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

  def search2(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
    res = []
    currexp = 0
    if len(init) == 1:
      # One agent only. FIXME
      # BFS
      queue = [] # nodes to expand
      status = {}
      #{
      #  vertex_number: {
      #    visited: boolean,
      #    parent: other_number,
      #    transport: 0..2,
      #    depth: 0,
      #    tickets: availableTickets
      #  }
      #}

      queue.append(init[0])
      status[init[0]] = {
        'visited': True,
        'parent': 0,
        'transport': -1,
        'depth': 0,
        'tickets': tickets
      }
      
      # while queue != []: # mais rapido
      while len(queue) > 0:
        curr = queue.pop(0)
        
        # print("U[",  curr, "] = ", self.model[curr])
        for i in self.model[curr]:
          transport, vertex = i
          if i[1] in status or status[curr]['tickets'][transport] == 0:
            continue

          newTickets = copy.deepcopy(status[curr]['tickets'])
          newTickets[transport] -= 1
          queue.append(vertex)
          status[vertex] = {
            'visited': True,
            'parent': curr,
            'transport': transport,
            'depth': status[curr]['depth'] + 1,
            'tickets': newTickets
          }

          if vertex == self.goal[0]:
            #printStatus(status)
            curr = self.goal[0]
            while curr != init[0]:
              res.insert(0, [[status[curr]['transport']], [curr]])
              curr = status[curr]['parent']
            res.insert(0, [[], [curr]])
            return res

        if (status[curr]['depth'] + 1) == limitdepth:
          return res
        
        currexp += 1
        if currexp == limitexp:
          return res
      return res

    else:
      if anyorder == True:
        pass

      #calculate heuristics
      numPoints = len(self.auxheur)
      straightLineDis1 =  [[]]
      straightLineDis2 = [[]]
      straightLineDis3 = [[]]

      for i in range(1, numPoints + 1):
        straightLineDis1.append(calcDist(self.auxheur, i-1, self.goal[0]-1))
        straightLineDis2.append(calcDist(self.auxheur, i-1, self.goal[1]-1))
        straightLineDis3.append(calcDist(self.auxheur, i-1, self.goal[2]-1))

      
      #Open lists
      queue1open = queue.PriorityQueue()
      queue2open = queue.PriorityQueue()
      queue3open = queue.PriorityQueue()


      #closed lists - made list for constant checking, putting and removing
      closedlist1 = [0] * numPoints + 1 
      closedlist2 = [0] * numPoints + 1
      closedlist3 = [0] * numPoints + 1

      # keep vertex cost, parent, transport, depth, tickets
      status1 = {}
      status2 = {}
      status3 = {}

      return res

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
      root = tuple(init)
      searchTree = {}
      searchTree[root] = {
          'parent': False,
          'typeTransport': [],
          'tickets': tickets,
          'stepCount': 0
      }

      # heap is a heap of tuples (heuristic, (position)) so we can compare combinations by their heuristic
      # position is a tuple so we can use the state combination as a dict key (see Advanced#4)
      heap = []
      heapq.heappush(heap, (self.score(searchTree[root]['stepCount'], init, self.goal), root))
      # print(heap)
      # print(searchTree)

      while(len(heap) > 0):
          #TODO: check limit depth and expansions
          curr = heapq.heappop(heap)[1]
          # print("===================Popped", curr)
          if curr == tuple(self.goal):
              return self.traceback(searchTree)

          # Generate possible moves
          # TODO: generate list of all combinations in one line (see Advanced#3)
          possibleMoves = []
          for pos in curr:
              # ---------- lines below only for debug
              # agentMoves = tuple(tuple(move) for move in self.model[pos]) # list of possible moves
              # print("Agent " + str(curr.index(pos)) + " position " + str(pos) + " : " + str(agentMoves))
              # ---------- lines above only for debug
              # TODO: filter bad moves (already visited, previous, no tickets for this trip, ...)
              # tuple(move) for move in self.model[pos] if <vertex is not visited, not previous...>
              possibleMoves.append(tuple(tuple(move) for move in self.model[pos]))
          
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
                  continue;
              
              if len(set(destVertices)) != len(move): # check rule#1
                  continue;

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
              # TODO: remove  ===================
              # printing all adjacent vertices
              _a = []
              for adj in self.model[curr]:
                  _a.append(adj[1])
              
              # print(curr, ":", _a)
              #==================================

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
