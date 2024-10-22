import sys
import os
import random
from collections import Counter
import numpy as np
from random import shuffle
import subprocess
gamma = 0.01
lambdaVal = 0.5

transitions = []

def getVals (filename):
    temp = []
    temp1 = []
    temp2 = []
    final = []
    lookupIndex = 0
    count = 0
    f = open(filename)
    for line in f:
        if (lookupIndex != 2500):
            if (count == transitions[lookupIndex] and count != 0):
                lookupIndex = lookupIndex + 1
                final.append(temp)
                counts.append(temp1)
                lengths.append(temp2)
                temp = []
                temp1 = []
                temp2 = []

            if (count == 0):
                lookupIndex = lookupIndex + 1

        temp.append(float(line))
        temp1.append(count)
        temp2.append(len(sentences[count]))

        count = count + 1

    final.append(temp)
    counts.append(temp1)
    lengths.append(temp2)

    f.close()
    return final

def getMaxVals():
    maxScores = []
    maxIndecies = []
    for i in range(0,len(stProbs)):
        maxScore = -1000000
        maxIndex = -1
        for j in range(0,len(stProbs[i])):
            score = ((1-lambdaVal) * tsProbs[i][j]) + (lambdaVal * stProbs[i][j]) + (gamma * lengths[i][j]) + (alpha * tfidf[i][j]) 

            if score > maxScore:
                maxScore = score
                maxIndex = j
            j = j + 1
        maxScores.append(maxScore)
        maxIndecies.append(maxIndex)
        i = i + 1

    f = open("rerankedTest.txt", "w")
    startIndex = 0
    for i in range(0, len(maxIndecies)):
        f.write(sentences[counts[i][maxIndecies[i]]])
        i = i + 1
    f.close()

    perl_script = subprocess.Popen("perl multi-bleu.perl test.tgt.txt < rerankedTest.txt > bleu.txt", shell = True)
    perl_script.communicate()
    f = open("bleu.txt")
    for line in f:
        start = line.index("=")
        end = line.index(",")
        bleu = float(line[start+2 : end])
        return bleu

number = 0
startIndex = 0
i = 0
f = open('index_valid.txt')
for line in f:
    if number != int(line):
        number = int(line)
        transitions.append(startIndex)
    startIndex = startIndex + 1
f.close()

sentences = []
f = open('rearank_target_valid.txt')
for line in f:
    sentences.append(line)

counts = []
lengths = []
tsProbs = getVals('t_given_s_valid.txt')
stProbs = getVals('s_given_t_valid.txt')
counts = []
lengths = []
tfidf = getVals('tfidf_valid.txt')
#glove = getVals('dev_src_glove_dist.txt')

alpha = 0.1
beta = 0.1
bleu = getMaxVals()
print bleu

