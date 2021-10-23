import VertexCover as vc
import Expe
import matplotlib.pyplot as plt

G = vc.readInstance("instance")

# G = vc.generateGraphe(15,0.3)
C = vc.couplageMax(G)
print(C)
C = vc.algo_glouton(G)
print(C)
C = vc.branchement_1(G)
print(C)
C = vc.branchement_Couplage(G, 0)
print(C)
C = vc.branchement_ameliore(G)
print(C)
C = vc.branchement_ameliore2(G)
print(C)
C = vc.branchement_ameliore3(G)
print(C)

# Expe.displayComplexFixedP2(vc.algo_glouton,vc.couplageMax,26,0.1,"test")
# plt.show()