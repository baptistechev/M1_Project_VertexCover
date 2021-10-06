
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

def displayComplex(fonction,nmax,title):
    plot1=plt.figure(title)

    x=np.arange(nmax/10,nmax,nmax/10)
    for p in np.arange (0.1,0.9,0.1):
        y=[]
        for i in range (nmax/10,nmax,nmax/10):
            sum=0
            for j in range (1,10):
                sum+=timeComplex(fonction,generateGraphe(i,p))
            y.append(sum/10)
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

def estFeuille(G):
    for s in G:
        if(len(G[s])==0) return False
    return True

def branchement_1(G):
    C=[]
    bestvalue=len(algo_glouton(G)) #on initialise le meilleurs nombre de sommet avec glouton
    pile=[]
    pile.append(G)
    for g in pile :
        if(not(estFeuille(G))): #il reste des arrête dans le graphe
            (u,v)
            for s in G:
                if (len(G[s]!=0)):#On prend le premier sommet avec des sommets ajd
                    (u,v)=(s,G[s][0])
                    break
            Gu=supprimerSommet(G,u) #Voir copy des graphes 
            Gv=supprimerSommet(G,v)
            pile.remove(g)
            pile.append(Gu) #A voir parcours de l'arbre
            pile.append(Gv)
        else: #plus d'arrête dans le graphe 
            


        





 