#
# Contient les fonctions sur les Graphes
#

# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import copy

#Permet de créer un graphe à partir d'un fichier
def readInstance(nomFichier):
    G = dict()
    f = open(nomFichier,"r")
    f.readline()
    n = int(f.readline())
    f.readline()
    for i in range(n):
        x = int(f.readline())
        G[i] = []
    f.readline()
    m = int(f.readline())
    f.readline()
    for i in range(m):
        l = f.readline()
        e = l.split(" ")
        u,v = int(e[0]), int(e[1])
        G[u].append(v)
        G[v].append(u)
    f.close()
    return G

#Supprime un sommet de G
def supprimerSommet(G, v):
    del G[v]
    for e in G:
        if v in G[e]:
            G[e].remove(v)
    return G

#Supprime un ensemble de sommets de G
def supprimerEnsembleSommet(G,V):
    for v in V:
        G = supprimerSommet(G,v)
    return G

#Retourne un tableau contenant les degrés de chaque sommets de G
def degSommets(g):
    deg=dict()
    for e in g:
        deg[e]=len(g[e])
    return deg
        
#Retourne le sommet de degré maximal de G
def degMax(g):
    deg=degSommets(g)
    m = list(deg.keys())[0]
    for e in deg:
        if deg[e]>=deg[m]:
            m=e
    return m

#Génère un graphe de n sommets avec probabilité de présence p pour chaque arête
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

#Retourne Vrai si G possède au moins une arête
def arete(G):
    for e in G:
        if(len(G[e])!=0):
            return True
    return False
    
#Algorithme Glouton
def algo_glouton(Graphe):
    G = copy.deepcopy(Graphe)
    C=[]
    while arete(G) :
        v = degMax(G)
        C.append(v)
        G=supprimerSommet(G,v)
    return C

#Algorithme de Couplage   
def couplageMax(G):
    C = []
    for x in G:
        if x not in C:
            for y in G[x]:
                if y not in C:
                    C.append(x)
                    C.append(y)
                    break 
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

#Algorithme de Branchement naïf
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

#Calcul la borne supérieure en utilisant Couplage ou Glouton et met à jour la meilleur solution
def calculBorneSup(G,C,flag):
    global bestCouverture

    if(flag==0 or flag==2 or flag==3 ):
        c = couplageMax(G) #Choix de la borne sup
    else:
        c=algo_glouton(G)

    for v in C:
        c.append(v)
    if len(c) < len(bestCouverture):
        bestCouverture = c
    return len(bestCouverture)

#Calcul la borne inférieure
def calculBorneInf(G,C,flag):
    if (flag==2):
        return len(C)
    else:
        n=len(G)
        m=0
        for g in G: 
            m+=len(G[g])
        m=m/2
        d=len(G[degMax(G)])

        b1= np.ceil(m/d) if d!=0 else 0
        b2=len(couplageMax(G))/2  
        b2 = 0
        b3=(2*n-1-np.sqrt((np.square(2*n-1)-8*m)))/2

        return len(C)+np.max([b1,b2,b3])

def branchement_aux_Couplage(G, C,flag):
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
    if(flag==3 ):
        borneSup=len(bestCouverture)
    else:
        borneSup = calculBorneSup(G,C,flag)

    borneInf = calculBorneInf(G,C,flag)


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
    branchement_aux_Couplage(G1, C1,flag)

    G2 = copy.deepcopy(G)
    C2 = copy.deepcopy(C)
    G2 = supprimerSommet(G2,v)
    C2.append(v)
    branchement_aux_Couplage(G2, C2,flag)

#Algorithme de branchement avec bornes
def branchement_Couplage(G,flag): #0:Coup 1:Glou 2:Coup/infT 3:Coup/supT
    global bestCouverture
    global  noeudGen
    global borneInf
    global borneSup
    noeudGen=1

    #Calcul bornes inf et sup
    bestCouverture = [g for g in G]
    borneSup = calculBorneSup(G,[],flag)
    borneInf = calculBorneInf(G,[],flag)

    #Si condition respect pas besoin d'aller plus loin
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
    branchement_aux_Couplage(supprimerSommet(G1,u), [u],flag)
    branchement_aux_Couplage(supprimerSommet(G2,v), [v],flag)

    print(noeudGen)
    return bestCouverture

########AMELIORATION BRANCHEMENT###########

bestCouverture = []
borneSup = 0
borneInf = 0

#Union de deux ensembles
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
    borneSup = calculBorneSup(G,C,0)
    borneInf = calculBorneInf(G,C,0)

    #Si condition respecte, on lague
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

#Première amélioration de branchement
def branchement_ameliore(G):
    global bestCouverture
    global  noeudGen
    global borneInf
    global borneSup
    noeudGen=1

    #Calcul bornes inf et sup
    bestCouverture = [g for g in G]
    borneSup = calculBorneSup(G,[],0)
    borneInf = calculBorneInf(G,[],0)

    #Si condition respect pas besoin d'aller plus loin
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

########AMELIORATION BRANCHEMENT 2###########
#Choix des aretes en fonction du degre des sommets

def branchement_aux_ameliore2(G, C):
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
    borneSup = calculBorneSup(G,C,0)
    borneInf = calculBorneInf(G,C,0)

    #Si condition respecte, on lague
    if(borneInf >= borneSup):
        return

    #sinon on selectionne une arete  de maniere a avoir u de degr max et on branche
    u = degMax(G)
    v = G[u][0]
    for x in G[u]:
        if len(G[x]) > len(G[v]):
            v = x

    noeudGen+=2

    G1 = copy.deepcopy(G)
    C1 = copy.deepcopy(C)   
    C1.append(u)

    G2 = copy.deepcopy(G)
    C2 = copy.deepcopy(C)
    C2.append(v)

    branchement_aux_ameliore2(supprimerEnsembleSommet(G1,Union([v], G[v])), Union(C1,G[v]))
    branchement_aux_ameliore2(supprimerEnsembleSommet(G2,Union([u], G[u])), Union(C2,G[u]))

#Deuxième amélioration de branchement
def branchement_ameliore2(G):
    global bestCouverture
    global noeudGen
    global borneInf
    global borneSup
    noeudGen=1

    #Calcul bornes inf et sup
    bestCouverture = [g for g in G]
    borneSup = calculBorneSup(G,[],0)
    borneInf = calculBorneInf(G,[],0)

    #Si condition respect pas besoin d'aller plus loin
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

    #On selectionne une arete dans G !! de mani  re a avoir u de degr max!!
    u = degMax(G)
    v = G[u][0]
    for x in G[u]:
        if len(G[x]) > len(G[v]):
            v = x

    #On branche sur chaque noeud
    noeudGen+=2
    G1 = copy.deepcopy(G)
    G2 = copy.deepcopy(G)

    branchement_aux_ameliore2(supprimerEnsembleSommet(G1,Union([v], G[v])), Union([u],G[v]))
    branchement_aux_ameliore2(supprimerEnsembleSommet(G2,Union([u], G[u])), Union([v],G[u]))

    print(noeudGen)
    return bestCouverture

########AMELIORATION BRANCHEMENT 3###########
#Suppression des sommets de dg 1

def branchement_aux_ameliore3(G, C):
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
    borneSup = calculBorneSup(G,C,0)
    borneInf = calculBorneInf(G,C,0)

    #Si condition respecte, on  lague
    if(borneInf >= borneSup):
        return

    #sinon on selectionne une arete !! de mani  re a avoir u de degr  max!! et on branche
    u = degMax(G)
    v = G[u][0]
    for x in G[u]:
        if len(G[x]) > len(G[v]):
            v = x

    noeudGen+=1
    G1 = copy.deepcopy(G)
    G2 = copy.deepcopy(G)

    C1 = copy.deepcopy(C)   
    C1.append(u)
    branchement_aux_ameliore3(supprimerEnsembleSommet(G1,Union([v], G[v])), Union(C1,G[v]))

    if len(G2[v]) > 1 : #Si le sommets v est de dg 1 pas beson de brancher
        noeudGen+=1
        C2 = copy.deepcopy(C)
        C2.append(v)
        branchement_aux_ameliore3(supprimerEnsembleSommet(G2,Union([u], G[u])), Union(C2,G[u]))

#Troisième amélioration de branchement
def branchement_ameliore3(G):
    global bestCouverture
    global noeudGen
    global borneInf
    global borneSup
    noeudGen=1

    #Calcul bornes inf et sup
    bestCouverture = [g for g in G]
    borneSup = calculBorneSup(G,[],0)
    borneInf = calculBorneInf(G,[],0)

    #Si condition respect  pas besoin d'aller plus loin
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

    #On selectionne une arete dans G !! de mani  re a avoir u de degr  max!!
    u = degMax(G)
    v = G[u][0]
    for x in G[u]:
        if len(G[x]) > len(G[v]):
            v = x

    #On branche sur chaque noeud

    noeudGen+=1
    G1 = copy.deepcopy(G)
    G2 = copy.deepcopy(G)
    branchement_aux_ameliore3(supprimerEnsembleSommet(G1,Union([v], G[v])), Union([u],G[v]))
    
    if len(G2[v]) > 1 : #Si le sommets v est de dg 1 pas besoin de brancher
        noeudGen+=1
        branchement_aux_ameliore3(supprimerEnsembleSommet(G2,Union([u], G[u])), Union([v],G[u]))
    
    print(noeudGen)
    return bestCouverture


 