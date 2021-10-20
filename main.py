import VertexCover as vc
import matplotlib.pyplot as plt
import numpy as np
import copy

G = vc.readInstance("instance")

#test 4.2
# G = {0 : [1,2], 1 : [0,4,3], 2 : [0],3:[4,1],4:[1,3]}

#contre exemple 4.3
# G = {0 : [1,2,3], 1 : [0,3,4], 2 : [0], 3 : [0,1], 4 : [1]}

# G = vc.generateGraphe(200,0.3)
C = vc.branchement_1(G)
print(C)
C = vc.branchement_Couplage(G)
print(C)
C = vc.branchement_ameliore(G)
print(C)
C = vc.branchement_ameliore2(G)
print(C)
C = vc.branchement_ameliore3(G)
print(C)

#C = vc.couplageMax(G)
#print(G)
#print(C)

#vc.coC=vc.algo_glouton(G)
#print(C)

#print(vc.timeComplex(vc.couplageMax,G))
#print(vc.timeComplex(vc.algo_glouton,G))

# vc.displayComplex(vc.algo_glouton,100,"glouton")
# vc.displayComplex(vc.couplageMax,100,"couplage")
# plt.show()

#print(vc.algo_glouton(G))
#C = vc.branchement_1(vc.generateGraphe(10,0.3))
#print(C)
#print("Noeud gen: ",vc.noeudGen)

#vc.displayComplex(vc.branchement_1,15,"Branchement dumb")
#plt.show()

# G=vc.generateGraphe(15,0.3)
# Gbis=copy.deepcopy(G)

#G={0: [3, 8], 1: [3, 8], 2: [6], 3: [0, 1], 4: [5, 8], 5: [4, 8], 6: [2], 7: [], 8: [0, 1, 4, 5]}
#print(G)
# print(1)
# print("SOL",vc.branchement_1(G))
# print(2)
# print("SOL",vc.branchement_Couplage(G))
# vc.displayComplex(vc.branchement_1,15,"Branchement couplage")
# plt.show()

