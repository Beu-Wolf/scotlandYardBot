import math
import pickle
import copy
import time

  
class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.goal = goal
    self.model = model
    self.auxheur = auxheur

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyOrder = False):
    res = []
    currexp = 0
    if len(init) > 1:
      print("Too many agents to handle... Grrr")
      return res
    
    
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

# TODO: Remove <3
def printStatus(status):
  for i in status.keys():
    print(i, status[i])
