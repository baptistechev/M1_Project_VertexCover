import VertexCover as vc

<<<<<<< HEAD
G = {1:[3],3:[1,2],2:[3]}

print(vc.degSommets(G))
print(vc.degMax(G))
=======
G = {0 : [1,2], 1 : [0], 2 : [0]}

print(G)
G = vc.supprimerEnsembleSommet(G, [1,2])
print(G)
>>>>>>> 0989a0ca9b065cd88d32892612624419161db986
