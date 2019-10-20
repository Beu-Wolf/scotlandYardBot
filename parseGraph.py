#!/usr/bin/env python3

import pickle

codes = {
    0: 'taxi',
    1: 'bus',
    2: 'subway'
}


with open("mapasgraph2.pickle", "rb") as fp:
    U = pickle.load(fp)[1]

# print(U)
for i in range(len(U)):
    print(i, ":", [codes[adj[0]] + " -> " + str(adj[1]) for adj in U[i]])

