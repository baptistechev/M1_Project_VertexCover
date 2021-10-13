
import numpy as np
import time 
import matplotlib.pyplot as plt
import copy

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

    x=np.arange(1,nmax)
    for p in np.arange (0.1,0.9,0.1):
        y=[]
        for i in range (1,nmax):
            sum=0
            for j in range (1,10):
                sum+=timeComplex(fonction,generateGraphe(i,p))
            y.append(sum/10)
        plt.plot(x,y,label = p)

    plt.xlabel('nb sommets')
    plt.ylabel('temps(s)')
    #plt.legend()
    return plot1   

def displayComplexFixedP(fonction,nmax,p,title):
    plot1=plt.figure(title)

    x=np.arange(1,nmax)
    
    y=[]
    for i in range (1,nmax):
        sum=0
        for j in range (1,60):
            sum+=timeComplex(fonction,generateGraphe(i,p))
        y.append(sum/60)
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

def algo_glouton(Graphe):
    G = copy.deepcopy(Graphe)
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


###########BRANCHEMENT#############
bestCouverture = []
noeudGen = 0

def branchement_aux_1(G, C):
    #print(G)

    global bestCouverture
    global noeudGen
    sommetsSup = []
    for g in G:
        if len(G[g]) == 0:
            sommetsSup.append(g)
    supprimerEnsembleSommet(G, sommetsSup)
    if len(G) == 0:
        if len(bestCouverture) > len(C):
            bestCouverture = C
    else:
        G1 = copy.deepcopy(G)
        G2 = copy.deepcopy(G)
        u = list(G.keys())[0]
        v = G[u][0]
        C1 = copy.deepcopy(C)
        C2 = copy.deepcopy(C)
        C1.append(u)
        noeudGen+=2
        branchement_aux_1(supprimerSommet(G1,u), C1)
        C2.append(v)
        branchement_aux_1(supprimerSommet(G2,v), C2)


def branchement_1(G):
    global bestCouverture
    global  noeudGen
    noeudGen=0
    bestCouverture = [g for g in G]
    sommetsSup = []
    for g in G:
        if len(G[g]) == 0:
            sommetsSup.append(g)
    supprimerEnsembleSommet(G, sommetsSup)
    if(len(G.keys()))==0:
        return G
    u = list(G.keys())[0]
    v = G[u][0]
    G1 = copy.deepcopy(G)
    G2 = copy.deepcopy(G)
    noeudGen+=2
    branchement_aux_1(supprimerSommet(G1,u), [u])
    branchement_aux_1(supprimerSommet(G2,v), [v])
    return bestCouverture

########BONRE INF###########

def calculBorneInf(G):
    n=len(G)
    m=0
    for g in G: 
        m+=len(G[g])
    m=m/2
    d=len(G[degMax(G)])
    if(d!=0): #Graphe vide 
        b1=np.ceil(m/d)
    else:
        b1=0
    b2=len(couplageMax(G))/2
    b3=(2*n-1-np.sqrt((np.square(2*n-1)-8*m)))/2

    return (b1,b2,b3)

def testBorneInf(C,G):
    (b1,b2,b3)=calculBorneInf(G)
    return len(C)+np.max([b1,b2,b3])<=len(bestCouverture)
        

def branchement_aux_Couplage(G, C):
    global bestCouverture
    global noeudGen
    sommetsSup = []
    for g in G:
        if len(G[g]) == 0:
            sommetsSup.append(g)
    supprimerEnsembleSommet(G, sommetsSup)
    if len(G) == 0:
        if len(bestCouverture) > len(C):
            bestCouverture = C
    else:
        G1 = copy.deepcopy(G)
        G2 = copy.deepcopy(G)
        u = list(G.keys())[0]
        v = G[u][0]
        C1 = copy.deepcopy(C)
        C2 = copy.deepcopy(C)

        G1 = supprimerSommet(G1,u)
        G2 = supprimerSommet(G2,v)

        C1.append(u)
        if(testBorneInf(C1,G1)):
            noeudGen+=1
            branchement_aux_Couplage(G1, C1)

        C2.append(v)
        if(testBorneInf(C2,G2)):
            noeudGen+=1  
            branchement_aux_Couplage(G2, C2)


def branchement_Couplage(G): #Faire un test de borne inf a l'init si on init a glouton ...
    global bestCouverture
    global  noeudGen
    noeudGen=0
    bestCouverture = [g for g in G]
    sommetsSup = []
    for g in G:
        if len(G[g]) == 0:
            sommetsSup.append(g)
    supprimerEnsembleSommet(G, sommetsSup)
    if(len(G.keys()))==0:
        return G
    u = list(G.keys())[0]
    v = G[u][0]
    G1 = copy.deepcopy(G)
    G2 = copy.deepcopy(G)
    noeudGen+=2
    branchement_aux_Couplage(supprimerSommet(G1,u), [u])
    branchement_aux_Couplage(supprimerSommet(G2,v), [v])

    return bestCouverture





 