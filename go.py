import pickle
import math
import copy
import matplotlib.pyplot as plt
import time
from solve import SearchProblem

with open("coords.pickle", "rb") as fp:   # Unpickling
    coords = pickle.load(fp)
    
with open("mapasgraph2.pickle", "rb") as fp:   #Unpickling
    AA = pickle.load(fp)
U = AA[1]

def ex1():
    print("\n(2 val) Exercise 1 - One agent, No limits")
    print("Init [30] Goal [56]")
    SP = SearchProblem(goal = [56], model = U, auxheur=coords)
    tinit = time.process_time()
    I = [30]
    nn = SP.search(I,limitexp = 2000)
    tend = time.process_time()
    print("%.1fms"%((tend-tinit)*1000))
    if validatepath(nn,I,U):   
            print("path")
            print(nn)
            plotpath(nn,coords)     
    else:
            print("invalid path")

def ex2():
    print("\n(4 val) Exercise 2 - One agent, Limits")
    print("Init [30] Goal [56]")
    SP = SearchProblem(goal = [56], model = U, auxheur=coords)
    tinit = time.process_time()
    I = [30]
    nn = SP.search(I,limitexp = 2000, tickets = [5,5,2])
    tend = time.process_time()
    print("%.1fms"%((tend-tinit)*1000))
    if validatepath(nn,I,U, tickets = [5,5,2]):
            print("path")
            print(nn)
            plotpath(nn,coords)
    else:
            print("invalid path")

def ex3_1():
    print("\n(6 val) Exercise 3 - Three agents, No limits (test 1)")
    print("Init [1,3,7] Goal [2,21,9]")
    SP = SearchProblem(goal = [2,21,9], model = U, auxheur=coords)
    tinit = time.process_time()
    I = [1,3,7]
    nn = SP.search(I,limitexp = 2000)
    tend = time.process_time()
    print("%.1fms"%((tend-tinit)*1000))
    if validatepath(nn,I,U):
            print("path")
            print(nn)
            plotpath(nn,coords)
    else:
            print("invalid path")

def ex3_2():
    print("\n(6 val) Exercise 3 - Three agents, No limits (test 2)")
    print("Init [30,40,109] Goal [61,60,71]")
    SP = SearchProblem(goal = [61,60,71], model = U, auxheur=coords)
    tinit = time.process_time()
    I = [30,40,109]
    nn = SP.search(I,limitexp = 2000)
    tend = time.process_time()
    print("%.1fms"%((tend-tinit)*1000))
    if validatepath(nn,I,U):
            print("path")
            print(nn)
            plotpath(nn,coords)
    else:
            print("invalid path")
        
def ex4():
    print("\n(4 val) Exercise 4 - Three agents, Limits")
    print("Init [30,40,109] Goal [63, 61, 70]")
    SP = SearchProblem(goal = [63,61,70], model = U, auxheur=coords)
    tinit = time.process_time()
    I = [30,40,109]
    nn = SP.search(I,limitexp = 3000, limitdepth = 10, tickets = [5,20,2])
    tend = time.process_time()
    print("%.1fms"%((tend-tinit)*1000))
    if validatepath(nn,I,U, tickets = [5,20,2]):
            print("path")
            print(nn)
            plotpath(nn,coords)
    else:
            print("invalid path")

def ex5():
    print("\n(4 val) Exercise 5 - Three agents, Limits, Any-Order")
    print("Init [30,40,109] Goal [63, 61, 70]")
    SP = SearchProblem(goal = [63,61,70], model = U, auxheur=coords)
    tinit = time.process_time()
    I = [30,40,109]
    nn = SP.search(I,limitexp = 3000, limitdepth = 10, tickets = [5,20,2], anyorder = True)
    tend = time.process_time()
    print("%.1fms"%((tend-tinit)*1000))
    if validatepath(nn,I,U, tickets = [5,20,2]):
        print("path")
        print(nn)
        plotpath(nn,coords)
    else:
        print("invalid path")




def plotpath(P,coords):   
        return
        img = plt.imread('maps.png')
        plt.imshow(img)
        colors = ['r.-','g+-','b^-']
        I = P[0][1]
        for agind in range(len(P[0][1])):
                st = I[agind]-1
                for tt in P:                        
                        nst = tt[1][agind]-1
                        plt.plot([coords[st][0],coords[nst][0]],[coords[st][1],coords[nst][1]],colors[agind])
                        st = nst
        plt.axis('off')
        fig = plt.gcf()
        fig.set_size_inches(1.*18.5, 1.*10.5)
        #fig.savefig('test2png.png', dpi=100)   
        plt.show()
        
def validatepath(oP,oI,U,tickets=[25,25,25]): 
        if not oP:
                return False
        P = copy.deepcopy(oP)
        I = copy.copy(oI)
        mtickets = copy.copy(tickets)

        # print(I)
        # print(P[0][1])
        if I!=P[0][1]:
                print('path does not start in the initial state')
                return False
        del P[0]
        
        for tt in P:
                for agind,ag in enumerate(tt[1]):
                        #print(ag)
                        st = I[agind]
                        if mtickets[tt[0][agind]]==0:
                                print(tt)
                                print('no more tickets')
                                return False
                        else:
                                mtickets[tt[0][agind]] -= 1
                                
                                if [tt[0][agind],ag] in U[st]:
                                        I[agind] = ag
                                        #pass
                                else:
                                        print(tt,agind)
                                        print('invalid action')
                                        return False
                if(len(set(I))<3) and len(I)==3:
                        print(tt)
                        print('there is more than one police in the same location')
                        return False
        # print(oP)
        return True

def go(val, exNum, desc, init, goal, tickets = [math.inf, math.inf, math.inf], limexp = 3000, limdepth = 10, anyorder = False):
    print("\n(" + str(val) + " val) Exercise " + str(exNum) + " - " + desc + (", Anyorder" if anyorder else ""))
    print(init, "to", goal, "with", tickets)
    SP = SearchProblem(goal = [*goal], model = U, auxheur=coords)
    I = [*init]
    tinit = time.process_time()
    nn = SP.search(I,limitexp = limexp, limitdepth = limdepth, tickets = tickets, anyorder = anyorder)
    tend = time.process_time()
    print("%.1fms"%((tend-tinit)*1000))
    if validatepath(nn,I,U, tickets = tickets):
        print("Path " + "(" + str(len(nn) - 1) + "):", nn)
        # plotpath(nn,coords)
    else:
        print("invalid path")

tinittotal = time.process_time()
# ex1()
go(2, 1, "One agent, No limits", [30], [56])
go(2, 1, "One agent, No limits, Reverse", [56], [30])

# ex2()
go(4, 2, "One agent, Limits", [30], [56], tickets = [5, 5, 2])
go(4, 2, "One agent, Limits, Reverse", [56], [30], tickets = [5, 5, 2])

# ex3_1()
go(6, 3, "Three agents, No limits (test 1)", [1, 3, 7], [2, 21, 9])
go(6, 3, "Three agents, No limits (test 1), Reverse", [2, 21, 9], [1, 3, 7])

# ex3_2()
go(6, 3, "Three agents, No limits (test 2)", [30, 40, 109], [61, 60, 71])
go(6, 3, "Three agents, No limits (test 2), Reverse", [61, 60, 71], [30, 40, 109])

# ex4()
go(4, 4, "Three agents, Limits", [30, 40, 109], [63, 61, 70], tickets = [5, 20, 2])
go(4, 4, "Three agents, Limits, Reverse", [63, 61, 70], [30, 40, 109], tickets = [5, 20, 2])

# ex5()
go(4, 5, "Three agents, Limits", [30, 40, 109], [63, 61, 70], tickets = [5, 20, 2], anyorder = True)
go(4, 5, "Three agents, Limits, Reverse", [63, 61, 70], [30, 40, 109], tickets = [5, 20, 2], anyorder = True)

print("\n=======ENTERING CUSTOM TESTS========")
go(math.inf, 6, "Three agents, Limits", [2, 10, 70], [113, 110, 2], tickets = [15, 10, 8])
go(math.inf, 6, "Three agents, Limits, Reverse", [113, 110, 2], [2, 10, 70], tickets = [15, 10, 8])

go(math.inf, 7, "Three agents, Limits (test 1)", [2, 10, 70], [113, 110, 2], tickets = [15, 10, 8], anyorder = True)
go(math.inf, 7, "Three agents, Limits (test 1), Reverse", [113, 110, 2], [2, 10, 70], tickets = [15, 10, 8], anyorder = True)

go(math.inf, 8, "Three agents, Limits", [34, 101, 48], [39, 32, 60], tickets = [15, 10, 8])
go(math.inf, 8, "Three agents, Limits", [39, 32, 60], [34, 101, 48], tickets = [15, 10, 8])

go(math.inf, 9, "Three agents, Limits", [34, 101, 48], [39, 32, 60], tickets = [15, 10, 8], anyorder = True)
go(math.inf, 9, "Three agents, Limits", [39, 32, 60], [34, 101, 48], tickets = [15, 10, 8], anyorder = True)

go(math.inf, 10, "Three agents, Limits", [57, 38, 112], [16, 108, 70], tickets = [15, 10, 8])
go(math.inf, 10, "Three agents, Limits", [16, 108, 70], [57, 38, 112], tickets = [15, 10, 8])

go(math.inf, 11, "Three agents, Limits", [57, 38, 112], [16, 108, 70], tickets = [15, 10, 8], anyorder = True)
go(math.inf, 11, "Three agents, Limits", [16, 108, 70], [57, 38, 112], tickets = [15, 10, 8], anyorder = True)


tendtotal = time.process_time()
print("Total time %.1fms"%((tendtotal-tinittotal)*1000))
