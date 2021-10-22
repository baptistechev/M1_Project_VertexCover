
# -*- coding: utf-8 -*-
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
    return (time.time()-start_time,ret)

def displayComplex(fonction,nmax,title):
    plot1=plt.figure(title)
    ax = plt.subplot(111)

    x=np.arange(nmax/10,nmax+(nmax/10),nmax/10)
    for p in np.arange (0.2,0.8,0.2):
        y=[]
        for i in range (nmax/10,nmax+(nmax/10),nmax/10):
            sum=0
            for j in range (0,10): 
                (t,C)=timeComplex(fonction,generateGraphe(i,p))
                sum+=t
            y.append(sum/10)
            (x2,y2)=(np.log(nmax),np.log(y[len(y)-1]))
            (x1,y1)=(np.log(nmax/10),np.log(y[0]))
        #lb="p="+str(p)+"\na="+str(np.around(((y2-y1)/(x2-x1)),2))
        lb="p="+str(p)
        ax.plot(x,y, label=lb)
        #ax.plot(np.log(x),np.log(y),label=lb)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    ax.legend(loc='lower left', bbox_to_anchor=(1, 0.1))

    #plt.title("Glouton | Equation: y=ax+b")
    plt.title("Branchement naif")
    plt.xlabel('x=n (nb de sommets)')
    plt.ylabel('y=t (temps s)')
    #plt.legend()
    return plot1 

def displayComplexFixedP(fonction,nmax,p,title):
    plot1=plt.figure(title)
    ax = plt.subplot(111)
    ax2 = ax.twinx()

    x=np.arange(nmax/10,nmax+(nmax/10),nmax/10)
    lb=""
    y=[]
    for i in range (nmax/10,nmax+(nmax/10),nmax/10):
        print("i="+str(i))
        sum=0
        coverMoy=0.0
        noeuds=0
        for j in range (0,10): 
            (t,C)=timeComplex(fonction,generateGraphe(i,p))
            noeuds+=noeudGen
            sum+=t
            coverMoy+=len(C)
        y.append(sum/10)
        lb+="n="+str(i)+"| Noeud: "+str(np.around(noeuds/10,0))+"\n"
        #coverMoy/=10
        #nbCoverMoy+=coverMoy/i
        
    #nbCoverMoy/=10
    (x2,y2)=(nmax,np.log(y[len(y)-1]))
    (x1,y1)=(nmax/10,np.log(y[0]))
    lbl="log(y)=ax+b | a="+str(np.around(((y2-y1)/(x2-x1)),2))
    
    #lb="p="+str(p)+"\nk="+str(np.around(nbCoverMoy,4))
    ax.plot(x,y,color='r',label=lb)
    ax2.plot(x,np.log(y),label=lbl, color='g')

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1, box.height])
    ax.legend(loc='lower right', bbox_to_anchor=(0.3, 0.5))

    ax.set_xlabel('x=n (nb sommets)')
    ax.set_ylabel('y-1=t (temps s)')

    ax2.set_ylabel('y-2= log(t)')

    plt.title("Branchement naif")
    #plt.xlabel('x=n (nb sommets)')
    #plt.ylabel('y=t (temps s)')
    plt.legend()
    return plot1 
       
def displayComplexFixedP4(fonction1,fonction2,fonction3,nmax,p,title):
    plot1=plt.figure(title)
    ax = plt.subplot(111)
    x=np.arange(nmax/10,nmax+(nmax/10),nmax/10)
    y1=[]
    y2=[]    
    y3=[]

    lb1="Amelioraiton 1:\n"
    lb2="Amelioration 2:\n"
    lb3="Amelioration 3:\n"

    for i in range (nmax/10,nmax+(nmax/10),nmax/10):
        sum1=0
        sum2=0
        sum3=0

        coverMoy1=0.0
        coverMoy2=0.0
        coverMoy3=0.0
        coverMoy0=0.0

        noeud1=0
        noeud2=0
        noeud3=0

        r1=0.0
        r2=0.0
        r3=0.0


        for j in range (0,10): 
            G=generateGraphe(i,p)
            (t1,C1)=timeComplex(fonction1,G)
            noeud1+=noeudGen
            (t2,C2)=timeComplex(fonction2,G)
            noeud2+=noeudGen
            (t3,C3)=timeComplex(fonction3,G)
            noeud3+=noeudGen

            (to,Co)=timeComplexBranch(G,0)
            sum1+=t1
            sum2+=t2
            sum3+=t3

            coverMoy1+=len(C1)
            coverMoy2+=len(C2)
            coverMoy3+=len(C3)
            coverMoy0+=len(Co)
            if(coverMoy0!=0):
                r1+=coverMoy1/(coverMoy0)
                r2+=coverMoy2/(coverMoy0)
                r3+=coverMoy3/(coverMoy0)
            else:
                r1+=1
                r2+=1
                r3+=1

        y1.append(sum1/10)
        y2.append(sum2/10)
        y3.append(sum3/10)
        
        lb1+=("n="+str(i)+" | r="+str(np.around(r1/10,2))+"| Noeud:"+str(noeud1/10)+"\n")
        lb2+=("n="+str(i)+" | r="+str(np.around(r2/10,2))+"| Noeud:"+str(noeud2/10)+"\n")
        lb3+=("n="+str(i)+" | r="+str(np.around(r3/10,2))+"| Noeud:"+str(noeud3/10)+"\n")

    (x2,k2)=(np.log(nmax),np.log(y1[len(y1)-1]))
    (x1,k1)=(np.log(nmax/10),np.log(y1[0]))
    (x4,k4)=(np.log(nmax),np.log(y2[len(y2)-1]))
    (x3,k3)=(np.log(nmax/10),np.log(y2[0]))
    (x6,k6)=(np.log(nmax),np.log(y3[len(y3)-1]))
    (x5,k5)=(np.log(nmax/10),np.log(y3[0]))
    #lb1+="a="+str(np.around(((k2-k1)/(x2-x1)),2))
    #lb2+="a="+str(np.around(((k4-k3)/(x4-x3)),2))
    #lb3+="a="+str(np.around(((k6-k5)/(x6-x5)),2))
    
    #lb1="k="+str(np.around(c,4))
    #lb2="k="+str(np.around(nbCoverMoy,4))
    ax.plot(x,y1,label=lb1)
    ax.plot(x,y2,label=lb2)
    ax.plot(x,y3,label=lb3)

    #ax.plot(np.log(x),np.log(y),label=lb)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='lower left', bbox_to_anchor=(1, -0.1))

    plt.title("Comparaison p="+str(p))
    plt.xlabel('x=n')
    plt.ylabel('y=t')
    #plt.legend()
    return plot1 

def displayComplexFixedP2(fonction1,fonction2,nmax,p,title):
    plot1=plt.figure(title)
    ax = plt.subplot(111)
    x=np.arange(nmax/10,nmax+(nmax/10),nmax/10)
    y1=[]
    y2=[]    

    lb1="Glouton p="+ str(p)+":\n"
    lb2="Couplage p=" + str(p)+":\n"

    

    for i in range (nmax/10,nmax+(nmax/10),nmax/10):
        sum1=0
        sum2=0
        r1=0.0
        r2=0.0

        coverMoy1=0.0
        coverMoy2=0.0
        coverMoy0=0.0

        for j in range (0,10): 
            G=generateGraphe(i,p)
            (t1,C1)=timeComplex(fonction1,G)
            (t2,C2)=timeComplex(fonction2,G)
            (to,Co)=timeComplexBranch(G,0)
            sum1+=t1
            sum2+=t2

            coverMoy1=len(C1)
            coverMoy2=len(C2)
            coverMoy0=len(Co)

            if(coverMoy0!=0):
                r1+=coverMoy1/(coverMoy0)
                r2+=coverMoy2/(coverMoy0)
            else:
                r1+=1
                r2+=1

        y1.append(sum1/10)
        y2.append(sum2/10)

        lb1+=("n="+str(i)+" | r="+str(np.around(r1/10,4))+"\n")
        lb2+=("n="+str(i)+" | r="+str(np.around(r2/10,2))+"\n")


    #lb="p="+str(p)+"\na="+str(np.around(((y2-y1)/(x2-x1)),2))
    #lb1="k="+str(np.around(c,4))
    #lb2="k="+str(np.around(nbCoverMoy,4))
    line,=ax.plot(x,y1,label=lb1)
    line,=ax.plot(x,y2,label=lb2)

    #ax.plot(np.log(x),np.log(y),label=lb)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    #ax.legend(loc='lower left', bbox_to_anchor=(1, -0.1))
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=2, fancybox=True, shadow=True)
    plt.title("Comparaison p="+str(p))
    plt.xlabel('x=n (nb sommets)')
    plt.ylabel('y=t (temps s)')
    #plt.legend()
    return plot1 

def timeComplexBranch(G,flag):
    start_time=time.time()
    ret=branchement_Couplage(G,flag)
    return (time.time()-start_time,ret)

def displayComplexBranch(nmax,p,title):
    plot1=plt.figure(title)
    ax = plt.subplot(111)
    #ax2 = ax.twinx()

    x=np.arange(nmax/10,nmax+(nmax/10),nmax/10)
    y1=[]
    y2=[]
    y3=[]
    #y4=[]
    lb1="Sup:C | Inf:C\n"
    lb2="Sup:C | Inf:T\n"
    lb3="Sup:T | Inf:C\n"

    #lb3="Sup:C | Inf:T\n"
    #lb4="Sup:G | Inf:T\n"

    for i in range (nmax/10,nmax+(nmax/10),nmax/10):
        print("i="+str(i))
        sum1=0
        sum2=0
        sum3=0

        noeud1=0
        noeud2=0
        noeud3=0

        #sum3=0
        #sum4=0
        coverMoy1=0.0
        coverMoy2=0.0
        #coverMoy3=0.0
        #coverMoy4=0.0
        for j in range (0,10): 
            G=generateGraphe(i,p)
            (t1,C1)=timeComplexBranch(G,0)
            noeud1+=noeudGen
            (t2,C2)=timeComplexBranch(G,2)
            noeud2+=noeudGen
            (t3,C3)=timeComplexBranch(G,3)
            noeud3+=noeudGen
            #(t3,C3)=timeComplexBranch(G,2)
            #(t4,C4)=timeComplexBranch(G,3)
            
            sum1+=t1
            sum2+=t2
            sum3+=t3
            #sum4+=t4

            coverMoy1+=len(C1)
            coverMoy2+=len(C2)
            #coverMoy3+=len(C3)
            #coverMoy4+=len(C4)

        y1.append(sum1/10)
        y2.append(sum2/10)
        y3.append(sum3/10)

        #y4.append(sum4/10)

        lb1+=("n="+str(i)+"| Noeuds :"+str(np.around((noeud1/10),0))+"\n")
        lb2+=("n="+str(i)+"| Noeuds :"+str(np.around((noeud2/10),0))+"\n")
        lb3+=("n="+str(i)+"| Noeuds :"+str(np.around((noeud3/10),0))+"\n")
        #lb4+=("n="+str(i)+" | c="+str(coverMoy4/10)+"\n")
    
    (x2,k2)=(nmax,np.log(y1[len(y1)-1]))
    (x1,k1)=(nmax/10,np.log(y1[0]))
    (x4,k4)=(nmax,np.log(y2[len(y2)-1]))
    (x3,k3)=(nmax/10,np.log(y2[0]))
        
    lbl1="Sup:C | Inf:C\n"+"log(y)=ax+b | a="+str(np.around(((k2-k1)/(x2-x1)),2))
    lbl2="Sup:G | Inf:C\n"+"log(y)=ax+b | a="+str(np.around(((k4-k3)/(x4-x3)),2))
    #lb="p="+str(p)+"\na="+str(np.around(((y2-y1)/(x2-x1)),2))
    #lb1="k="+str(np.around(c,4))
    #lb2="k="+str(np.around(nbCoverMoy,4))
    line, = ax.plot(x,y1,label=lb1, color='b')
    line, = ax.plot(x,y2,label=lb2, color='y')
    line, = ax.plot(x,y3,label=lb3, color='g')

    #ax2.plot(x,np.log(y1),label=lbl1, color='r')
    #ax2.plot(x,np.log(y2),label=lbl2, color='g')

    #line, = ax.plot(x,y3,label=lb3)
    #line, = ax.plot(x,y4,label=lb4)

    #ax.plot(np.log(x),np.log(y),label=lb)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='lower left', bbox_to_anchor=(1, 0))
    #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    #ax.legend(loc='lower right', bbox_to_anchor=(1, 0.1))
    #ax.legend(loc='upper right', bbox_to_anchor=(0.5, 1.05),
    #     ncol=4, fancybox=True, shadow=True)
    plt.title("Comparaison p="+str(p))
    ax.set_xlabel('x=n (nb sommets)')
    ax.set_ylabel('y=t (temps s)')
    #ax2.set_ylabel('y-2= log(t)')
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

def arete(G):
    for e in G:
        if(len(G[e])!=0):
            return True
    return False
    
def algo_glouton(Graphe):
    G = copy.deepcopy(Graphe)
    C=[]
    while arete(G) :
        v = degMax(G)
        C.append(v)
        G=supprimerSommet(G,v)
    return C
    

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

def branchement_Couplage(G,flag): #0:Coup/inf 1:Glou/inf 2:Coup 3:Glou
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


 