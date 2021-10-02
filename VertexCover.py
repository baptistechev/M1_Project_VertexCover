
import numpy as np
import time 
import matplotlib.pyplot as plt

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

def timeComplex(fonction,G):
    start_time=time.time()
    ret=fonction(G)
    return time.time()-start_time

def displayComplex(fonction,r,title):
    plot1=plt.figure(title)

    x=np.arange(1,r)
    for p in np.arange (0.1,0.9,0.1):
        y=[]
        for i in range (1,r):
            y.append(timeComplex(fonction,generateGraphe(i,p)))
        plt.plot(x,y,label = p)

    plt.xlabel('nb sommets')
    plt.ylabel('temps(s)')
    #plt.legend()
    return plot1   
    


def generateGraphe(n,p):
    G = dict()
    for i in range(n):
        G[i] = []
    for i in range(n):
        for j in range(i,n):
            if j!=i and np.random.rand() < p:
                G[i].append(j)
                G[j].append(i)
    return G

def algo_glouton(G):
    C=[]
    while G :
        v = degMax(G)
        C.append(v)
        G=supprimerSommet(G,v)
    return C
    

def couplageMax(G):
    C = []
    for x in G:
        for y in G[x]:
            if x not in C and y not in C:
                C.append(x)
                C.append(y)
    return C


 