#!/usr/bin/env python
from igraph import *
import networkx as nx

import inspect
import itertools
import glob
import math

def benchmark(xarxa,llistacomunitats):
    #Per tal de comparar les comunitats calculades ho tenim de fer a partir d'una 
    #particio de referencia o particio que es consideri com a real o "bona".
    #Com que no es pot fer de forma "automatica" farem que l'usuari determini quina es la referent
    print "\nEsculli la particio que s'utilitzara com a referent"
    print "o carregui la particio d'un arxiu que vulgui utilitzar com a referent\n"
    print '\nParticions disponibles dels algorismes calculats:'
    con=0
    i=0
    while(i != len(llistacomunitats)):
        print '[',i,']', llistacomunitats[i]
        i+=2
        con+=1
    
    referent = '' # string de l'algorisme referent
    
    ca = raw_input("\nEscriu el numero de l'algorisme o escriu 'arxiu' per carregar un arxiu dels disponibles:\n")
    if ca == 'arxiu':
        print "\nSeleccioni un dels arxius a carregar"
        print "S'ha de tenir en compte la xarxa actual carregada, no carregar una particio d'una altre xarxa\n"
        print "Els arxius es busquen a la carpeta anomenada 'comunitats':\n"
        
        ruta = glob.glob('./comunitats/*.*') #troba la ruta dels arxius que indiquem
            
        print "\nParticions disponibles a la carpeta comunitats:"
            
        llista = []
            
        for i in range(len(ruta)):
            stemp = ruta[i].split('/')
            #print stemp
            semp = stemp[2].split('.')
            #print semp
            print semp[0]
            llista.append(semp[0])
        conta = 1
        #for y in range(len(llista)):
        #    if llista[y][0]!=llista[y-1][0]:
        #        print '[',conta,']',llista[y][0]
        #        #print 'disponible en format: ',llista[y][1]
        #        conta+=1 #per tal de que el numero de xarxa apareixi correcte
        #    else:
        #        print '                      ',llista[y][1]
        #    
        nb = raw_input("\nEscriu el nom de la xarxa a llegir\n")
        linia =[]
        member = []
        with open ('./comunitats/'+nb+'.txt','r') as f:
            read_line = f.readline()
            #print read_line
            #lines = f.readlines()
            #for line in lines:
            #    linia.append(line)
            #linia.append(lines)
        f.close()
        #print read_line
        
        llista = eval(read_line) #aixo es el membership de la comunitat
        #print llista
        #novalist = [int(n) for n in read_line.split(',')]
        #print novalist
        
        #for i in range(len(linia)):
        #    if linia[i]!="[" or linia[i]!="]" or linia[i]!="'" or linia[i]!="," or linia[i]!=' ':
        #        member.append(linia[i])
        #
        #print member
        vc = VertexClustering(xarxa,llista)
        print "L'algorisme referent es "+nb
        print "\nAmb la particio:"
        print vc
        referent = nb #nom de la particio de l'arxiu calculat
        comparador(referent,vc,llistacomunitats)
        
    elif ca == 'tornar':
        return
    elif(len(ca)!=1):
        print "S'ha d'escriure un numero dels algorismes o 'arxiu' per cargar un arxiu o 'tornar' per sortir al menu"
    else:
        cal = int(ca)
        memb0 = llistacomunitats[cal+1] #membership de l'algorisme
        referent = llistacomunitats[cal] #nom de l'algorisme
        comparador(referent,memb0,llistacomunitats)
    
    return

def comparador(referent,memb0,llistacomunitats):
    print '\nEsculli un algorisme dels de la llista per a realitzar la comparacio amb el referent\n'
    print '\nAlgorismes disponibles:'
    con=0
    i=0
    while(i != len(llistacomunitats)):
        print '[',i,']', llistacomunitats[i]
        i+=2
        con+=1
    
    sel = raw_input("\nIndiqui l'algorisme amb el numero\nO escriu 'tornar' per tornar al menu principal\n")
    
    if(sel =='tornar'):
        return
    else:
        se = int(sel)
        memb1 = llistacomunitats[se+1] #membership de l'algorisme a comparar
        comparat = llistacomunitats[se] #nom de l'algorisme comparat
        mesurador(referent,memb0,comparat,memb1,llistacomunitats)

    return

def mesurador(referent,memb0,comparat,memb1,llistacomunitats):
    print '\nEstem comparant la comunitat trobada amb',referent,' amb la',comparat
    print '\nEsculli la metrica que usar per realitzar la comparacio:\n'
    print '[1] Variation of information metric of Meila (2003)\n'
    #Variation of information
    #VI(X;Y)=H(X)+H(Y)-2I(X,Y) . H = entropy, I = mutual information.
    #In particular, it defines a metric in the space of partitions as it has the properties of distance.
    #The maximum value of the variation of information is log n, so similarity values for partitions
    #of graphs with different size cannot be compared with each other.
    #For meaningful comparisons one could divide V(X,Y) by log n (es el maxim), as suggested by Karrer et al. (Karrer et al., 2008).
    
    print '[2] Normalized mutual information as defined by Danon et al (2005)\n'
    #Normalized mutual information
    #The normalized mutual information equals 1 if the partitions are identical,
    #whereas it has an expected value of 0 if the partitions are independent.
    
    print '[3] Split-join distance of van Dongen (2000)\n'
    #Normalized Van Dongen metric
    #http://lists.gnu.org/archive/html/igraph-help/2010-07/msg00088.html
    #d(A,B) = 2n - Pa(B) - Pb(A
    #Performance Criteria for Graph Clustering and Markov Cluster Experiments (2000)
    #Similarity measures based on cluster matching aim at finding the largest overlaps between pairs of clusters of different partitions.
    #The split/join distance is easily interpretable as the number of
    #nodes that need changing to obtain one clustering from the other, and
    #fragmentation is in practice uncommon.    
    
    print '[4] Rand index of Rand (1971)\n'    
    #Rand index
    #http://en.wikipedia.org/wiki/Rand_index
    #Paper no disponible gratis
    #The Rand index has a value between 0 and 1, with 0 indicating
    #that the two data clusters do not agree on any pair of points and 1 indicating that the data clusters are exactly the same.    
    #Is the ratio of the number of vertex pairs correctly classified in both partitions
    
    print '[5] Adjusted Rand index of Hubert and Arabie (1985)\n'
    #Adjusted Rand index
    #http://en.wikipedia.org/wiki/Rand_index#Adjusted_Rand_index
    #ARI=(RI-E)/(1-E)
    #1 es el maxim de igual, 0 es totalment diferent
    #Paper no disponible gratis
    #Adjusted versions of both the Rand and the Jaccard in- dex exist, in that a null model is introduced, corresponding to the hypothesis of independence of the two partitions 
    
    ce = raw_input('Escriu els numeros dels parametres que vulguis amb una coma entre mig:\n')
    cel = ce.split(',')
    
    #n0 = int(sel[0])
    #n1 = int(sel[1])    
    
    for y in range(len(cel)):
        if cel[y] == "1":
            print '\n\tVariation of information metric of Meila :'
            resul = compare_communities(memb0,memb1,)
            print resul
            #num = len(memb0) #Karrer 2008
            #karrer = resul / (math.log10(num))
            print karrer
        if cel[y] == "2":
            print '\n\tNormalized mutual information as defined by Danon et al :'
            print compare_communities(memb0,memb1,"dannon")            
        if cel[y] == "3":
            print '\n\tSplit-join distance of van Dongen :'
            print compare_communities(memb0,memb1,"split-join")
        if cel[y] == "4":
            print '\n\tIndex of Rand :'
            print compare_communities(memb0,memb1,"rand")
        if cel[y] == "5":
            print '\n\tAdjusted Rand index of Hubert and Arabie :'
            print compare_communities(memb0,memb1,"adjusted_rand")    
    
    
    return
