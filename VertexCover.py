
import numpy as np

def degSommets(g):
    deg=[len(g)]
    cpt=0
    for e in g:
        deg[cpt]=len(e)
        cpt+=1
    return deg
        
def degMax(g):
    return np.maximum(degSommets(g))
    
    
 


