import VertexCover as vc

# G = {0 : [1,2], 1 : [0], 2 : [0]}

G = vc.generateGraphe(10,0.3)
C = vc.couplageMax(G)
print(G)
print(C)