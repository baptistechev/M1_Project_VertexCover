
import numpy as np

def supprimerSommet(G, v):
    del G[v]
    for e in G:
        if v in G[e]:
            G[e].remove(v)
    return G

def supprimerEnsembleSommet(G,V):
    for v in V:
        G = supprimerSommet(G,v)
    return G

def degSommets(g):
    deg=[len(g)]
    cpt=0
    for e in g:
        deg[cpt]=len(e)
        cpt+=1
    return deg
        
def degMax(g):
    return np.maximum(degSommets(g))

    
    
 


