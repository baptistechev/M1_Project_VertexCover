import VertexCover as vc
import matplotlib.pyplot as plt
import time
import numpy as np

#Calcul le temps d'éxécution de la fonction G
def timeComplex(fonction,G):
    start_time=time.time()
    ret=fonction(G)
    return (time.time()-start_time,ret)

#Affiche le temps d'execution d'une fonction en fonction du nombre de sommets
def displayComplex(fonction,nmax,title):
    plot1=plt.figure(title)
    ax = plt.subplot(111)

    x=np.arange(nmax/10,nmax+(nmax/10),nmax/10)
    for p in np.arange (0.2,0.8,0.2):
        y=[]
        for i in range (nmax/10,nmax+(nmax/10),nmax/10):
            sum=0
            for j in range (0,10): 
                (t,C)=timeComplex(fonction,vc.generateGraphe(i,p))
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

#Affiche le temps d'execution d'une fonction en fonction du nombre de sommets pour p fixe
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
            (t,C)=timeComplex(fonction,vc.generateGraphe(i,p))
            noeuds+=vc.noeudGen
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

#Affiche le temps d'execution de plusieurs fonctions en fonction du nombre de sommets pour p fixe
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
            G=vc.generateGraphe(i,p)
            (t1,C1)=timeComplex(fonction1,G)
            noeud1+=vc.noeudGen
            (t2,C2)=timeComplex(fonction2,G)
            noeud2+=vc.noeudGen
            (t3,C3)=timeComplex(fonction3,G)
            noeud3+=vc.noeudGen

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

#Affiche le temps d'execution de plusieurs fonctions en fonction du nombre de sommets pour p fixe
def displayComplexFixedP2(fonction1,fonction2,nmax,p,title):
    plot1=plt.figure(title)
    ax = plt.subplot(111)
    x= range(nmax//10,nmax+(nmax//10),nmax//10)
    print(x)
    y1=[]
    y2=[]    

    lb1="Glouton p="+ str(p)+":\n"
    lb2="Couplage p=" + str(p)+":\n"

    

    for i in x:
        sum1=0
        sum2=0
        r1=0.0
        r2=0.0

        coverMoy1=0.0
        coverMoy2=0.0
        coverMoy0=0.0

        for j in range (10): 
            G=vc.generateGraphe(i,p)
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
    ret=vc.branchement_Couplage(G,flag)
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
            G=vc.generateGraphe(i,p)
            (t1,C1)=timeComplexBranch(G,0)
            noeud1+=vc.noeudGen
            (t2,C2)=timeComplexBranch(G,2)
            noeud2+=vc.noeudGen
            (t3,C3)=timeComplexBranch(G,3)
            noeud3+=vc.noeudGen
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
