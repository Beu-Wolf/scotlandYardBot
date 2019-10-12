import math
import pickle
import copy
import time
import math
import queue

  
class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.goal = goal
    self.model = model
    self.auxheur = auxheur

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
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
      


# TODO: Remove <3
def printStatus(status):
  for i in status.keys():
    print(i, status[i])


def calcDist(auxheur, point, objective):
  x = auxheur[objective][0] - auxheur[point][0]
  y = auxheur[objective][1] - auxheur[point][1]

  return math.sqrt(x**2 + y**2)