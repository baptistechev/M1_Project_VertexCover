import VertexCover as vc

G = {0 : [1,2], 1 : [0], 2 : [0]}

print(G)
G = vc.supprimerEnsembleSommet(G, [1,2])
print(G)