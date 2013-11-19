# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:38:15 2013

@author: Abhishek
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
from os import listdir
from os.path import isfile, join



def createCharsfromFile(fname = 'license.txt'):
    fd = open(fname,'r')
    chars = ''
    for line in fd:
       for c in line:
           if (c.isalnum() or c == ' '):
               chars += c.lower()
    return chars
    
def createAlphabetsfromChars(chars):
    alphabets = list(set(chars))
    alphabets.sort()
    return alphabets
    
def createTransitionMatrix(chars,alphabets, threshold =  0.01):
    alphabetSize = len(alphabets)
    xp = chars[-1]
    transitionMatrix = zeros((alphabetSize,alphabetSize))
    
    for c in chars:
        i = alphabets.index(xp)
        j = alphabets.index(c)
        transitionMatrix[i][j] += 1
        xp = c
#    Pthresh = transitionMatrix/(np.sum(transitionMatrix,axis=0))
#    P = (transitionMatrix - mean(transitionMatrix))/std(transitionMatrix)
#    Pthresh = zeros((alphabetSize,alphabetSize))
#    i,j = 0,0
#    for x in P:
#        for y in x:
#            if (y > threshold):
#                Pthresh[i][j] = y
#            i += 1
#        j+= 1
#        i = 0
#    Pthresh = log(P+3)
    return transitionMatrix
    
def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"   
   
def randomwalk(P = zeros((2,2))+0.5, alphabets='01', iterations = 10, startchar='0'):
    sampleoutput = ''
    currentchar = startchar
    
    for i in range(0,iterations):
        sampleoutput += currentchar
        currentNodeTransitions = [x for x in itertools.izip(alphabets,P[alphabets.index(currentchar),:])]
        currentchar = weighted_choice(currentNodeTransitions)
    return sampleoutput
#################################################
#filesList = ['Sherlock.txt','HuckleberryFinn.txt','Contos.txt','license.txt','Charnet2.py']
filesList = ['abc.txt']
#onlyfiles = [ f for f in listdir('./Data') if isfile(join(mypath,f)) ]

for f in filesList:
    chars = createCharsfromFile(f)
    alphabets = createAlphabetsfromChars(chars)
    transMat = createTransitionMatrix(chars,alphabets)
    P = (transMat.T/np.sum(transMat.T,axis=0)).T  
#    figure(f)
#    plt.imshow(Pthresh, cmap = cm.Greys_r, interpolation = None)
    sampleoutput = randomwalk(P,alphabets,1000,alphabets[0])
    
    fo = open(f + 'out.txt','w')
    fo.write(sampleoutput)
    fo.close()  

#a=[i+'->'+j for i,j in itertools.product(alphabets,alphabets)]
G=nx.to_networkx_graph(P,create_using=nx.DiGraph())
nx.write_graphml(G,"charnet2.graphml")
nx.write_gml(G,"charnet2.gml")


