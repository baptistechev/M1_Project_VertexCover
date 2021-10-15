
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
    m = list(deg.keys())[0]
    for e in deg:
        if deg[e]>=deg[m]:
            m=e
    return m

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
    noeudGen=1
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

    print(noeudGen)
    return bestCouverture





########BRANCHEMENT BORNE###########

#Test a faire pour 4.2.3
#Uniquement borne sup
#Uniquement borne inf
#utiliser algo glouton pour borne sup

bestCouverture = []
borneSup = 0
borneInf = 0

def calculBorneSup(G,C):
    global bestCouverture
    c = couplageMax(G)
    for v in C:
        c.append(v)
    if len(c) < len(bestCouverture):
        bestCouverture = c
    return len(bestCouverture)

def calculBorneInf(G,C):
    n=len(G)
    m=0
    for g in G: 
        m+=len(G[g])
    m=m/2
    d=len(G[degMax(G)])

    b1= np.ceil(m/d) if d!=0 else 0
    # b2=len(couplageMax(G))/2  #vraiment couplage ?????????????? ensemble de sommets
    b2 = 0
    b3=(2*n-1-np.sqrt((np.square(2*n-1)-8*m)))/2

    return len(C)+np.max([b1,b2,b3])

def branchement_aux_Couplage(G, C):
    global bestCouverture
    global noeudGen
    global borneInf
    global borneSup

    sommetsSup = []
    for g in G:
        if len(G[g]) == 0:
            sommetsSup.append(g)
    supprimerEnsembleSommet(G, sommetsSup)

    if len(G) == 0:
        if len(bestCouverture) > len(C):
            bestCouverture = C
        return
    
    #calcul des bornes
    borneSup = calculBorneSup(G,C)
    borneInf = calculBorneInf(G,C)

    #Si condition respectée, on élague
    if(borneInf >= borneSup):
        return

    #sinon on selectionne une arete et on branche
    u = list(G.keys())[0]
    v = G[u][0]

    noeudGen+=2

    G1 = copy.deepcopy(G)
    C1 = copy.deepcopy(C)
    G1 = supprimerSommet(G1,u)    
    C1.append(u)
    branchement_aux_Couplage(G1, C1)

    G2 = copy.deepcopy(G)
    C2 = copy.deepcopy(C)
    G2 = supprimerSommet(G2,v)
    C2.append(v)
    branchement_aux_Couplage(G2, C2)


def branchement_Couplage(G):
    global bestCouverture
    global  noeudGen
    global borneInf
    global borneSup
    noeudGen=1

    #Calcul bornes inf et sup
    bestCouverture = [g for g in G]
    borneSup = calculBorneSup(G,[])
    borneInf = calculBorneInf(G,[])

    #Si condition respecté pas besoin d'aller plus loin
    if(borneInf >= borneSup):
        return bestCouverture

    #suppression des sommets sans voisins
    sommetsSup = []
    for g in G:
        if len(G[g]) == 0:
            sommetsSup.append(g)
    supprimerEnsembleSommet(G, sommetsSup)
    if len(G)==0:
        return []

    #On selectionne une arete dans G
    u = list(G.keys())[0]
    v = G[u][0]

    #On branche sur chaque noeud
    noeudGen+=2
    G1 = copy.deepcopy(G)
    G2 = copy.deepcopy(G)
    branchement_aux_Couplage(supprimerSommet(G1,u), [u])
    branchement_aux_Couplage(supprimerSommet(G2,v), [v])

    print(noeudGen)
    return bestCouverture

########AMELIORATION BRANCHEMENT###########

bestCouverture = []
borneSup = 0
borneInf = 0

def Union(l1,l2):
    for e in l2:
        if e not in l1:
            l1.append(e)
    return l1

def branchement_aux_ameliore(G, C):
    global bestCouverture
    global noeudGen
    global borneInf
    global borneSup

    sommetsSup = []
    for g in G:
        if len(G[g]) == 0:
            sommetsSup.append(g)
    supprimerEnsembleSommet(G, sommetsSup)

    if len(G) == 0:
        if len(bestCouverture) > len(C):
            bestCouverture = C
        return
    
    #calcul des bornes
    borneSup = calculBorneSup(G,C)
    borneInf = calculBorneInf(G,C)

    #Si condition respectée, on élague
    if(borneInf >= borneSup):
        return

    #sinon on selectionne une arete et on branche
    u = list(G.keys())[0]
    v = G[u][0]

    noeudGen+=2

    G1 = copy.deepcopy(G)
    C1 = copy.deepcopy(C)   
    C1.append(u)

    G2 = copy.deepcopy(G)
    C2 = copy.deepcopy(C)
    C2.append(v)

    branchement_aux_ameliore(supprimerEnsembleSommet(G1,Union([v], G[v])), Union(C1,G[v]))
    branchement_aux_ameliore(supprimerEnsembleSommet(G2,Union([u], G[u])), Union(C2,G[u]))


def branchement_ameliore(G):
    global bestCouverture
    global  noeudGen
    global borneInf
    global borneSup
    noeudGen=1

    #Calcul bornes inf et sup
    bestCouverture = [g for g in G]
    borneSup = calculBorneSup(G,[])
    borneInf = calculBorneInf(G,[])

    #Si condition respecté pas besoin d'aller plus loin
    if(borneInf >= borneSup):
        return bestCouverture

    #suppression des sommets sans voisins
    sommetsSup = []
    for g in G:
        if len(G[g]) == 0:
            sommetsSup.append(g)
    supprimerEnsembleSommet(G, sommetsSup)
    if len(G)==0:
        return []

    #On selectionne une arete dans G
    u = list(G.keys())[0]
    v = G[u][0]

    #On branche sur chaque noeud
    noeudGen+=2
    G1 = copy.deepcopy(G)
    G2 = copy.deepcopy(G)

    branchement_aux_ameliore(supprimerEnsembleSommet(G1,Union([v], G[v])), Union([u],G[v]))
    branchement_aux_ameliore(supprimerEnsembleSommet(G2,Union([u], G[u])), Union([v],G[u]))

    print(noeudGen)
    return bestCouverture





 