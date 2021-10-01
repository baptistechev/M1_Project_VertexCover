
import numpy as np

def degSommets(g):
    deg=dict()
    for e in g:
        deg[e]=len(g[e])
    return deg
        
def degMax(g):
    deg=degSommets(g)
    init=False
    for e in deg:
        if not(init):
            max=e
            init=True
        if deg[e]>=deg[max]:
            max=e
    return max


    
 


