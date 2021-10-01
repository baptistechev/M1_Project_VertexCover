import VertexCover as vc

# G = {0 : [1,2], 1 : [0], 2 : [0]}

G = vc.generateGraphe(1000,0.3)
#C = vc.couplageMax(G)
#print(G)
#print(C)

#vc.coC=vc.algo_glouton(G)
#print(C)

print(vc.timeComplex(vc.couplageMax,G))
print(vc.timeComplex(vc.algo_glouton,G))