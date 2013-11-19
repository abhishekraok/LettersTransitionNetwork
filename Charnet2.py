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
import itertools
import random

#returns string of characters from given text filename
def createCharsfromFile(fname = 'license.txt'):
    fd = open(fname,'r')
    chars = ''
    for line in fd:
       for c in line:
           allowedchars = [' ', '"', '#', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '5', '6', '8', ':', '=', '>', '@', '[', ']', '_']
           if (c.isalnum() or (c in allowedchars)):
               chars += c.lower()
    return chars
    
#Returns a sorted list of unique characters from input string
def createAlphabetsfromChars(chars):
    alphabets = list(set(chars))
    alphabets.sort()
    return alphabets

#Returns a transition count matrix from the given string
#aij is the count of times character j comes after character i
def createTransitionMatrix(chars,alphabets):
    alphabetSize = len(alphabets)
    xp = chars[-1]
    transitionMatrix = zeros((alphabetSize,alphabetSize)) 
    for c in chars:
        i = alphabets.index(xp)
        j = alphabets.index(c)
        transitionMatrix[i][j] += 1
        xp = c
    return transitionMatrix

#PMF sample output. Thanks to Lipis from stackoverflow.com
def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"   

#Returns sample output of iterations size given transition probability matrix P
def randomwalk(P = zeros((2,2))+0.5, alphabets='01', iterations = 10, startchar='0'):
    sampleoutput = ''
    currentchar = startchar
    
    for i in range(0,iterations):
        sampleoutput += currentchar
        currentNodeTransitions = [x for x in itertools.izip(alphabets,P[alphabets.index(currentchar),:])]
        currentchar = weighted_choice(currentNodeTransitions)
    return sampleoutput

#Returns networkx graph given matrix P
def createNetworkfromP(P,alphabets,threshold = 0.1):
    G = nx.DiGraph() 
    i,j = 0,0
    for x in P:
        for y in x:
            if (y > threshold):
                G.add_edge(alphabets[i],alphabets[j],weight = y)
            j += 1
        i+= 1
        j = 0
    return G


filesList = [ f for f in listdir('./Data') if isfile(join('./Data',f)) ]
for f in filesList:
    chars = createCharsfromFile('./Data/'+f)
    alphabets = createAlphabetsfromChars(chars)
    transMat = createTransitionMatrix(chars,alphabets)
    P = (transMat.T/np.sum(transMat.T,axis=0)).T  
    figure(f)
    fig = plt.imshow(P, cmap = cm.Greys_r, interpolation = "nearest")
    plt.xticks(range(len(P)),alphabets)  
    plt.yticks(range(len(P)),alphabets)
    plt.savefig('./outfig/'+f+'.out.png',dpi=300)
    plt.close()
    sampleoutput = randomwalk(P,alphabets,1000,alphabets[0])
    fo = open('./outtxt/'+f+'.out.txt','w')
    fo.write(sampleoutput)
    fo.close()  
    G = createNetworkfromP(P,alphabets)
    nx.write_gml(G,'./outnet/'+f+'.out.gml')


