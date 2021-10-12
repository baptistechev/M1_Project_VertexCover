import VertexCover as vc
import matplotlib.pyplot as plt

# G = {0 : [1,2], 1 : [0], 2 : [0]}
G = vc.generateGraphe(10,0.3)
C = vc.branchement_1(G)
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