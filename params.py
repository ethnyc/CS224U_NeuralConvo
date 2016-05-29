import sys
import os
import random
from collections import Counter
import numpy as np
from random import shuffle
import subprocess
gamma = -0.01
lambdaVal = 0.5
maxBleu = 0
maxBleuTest = 0
maxAlpha = -1
maxAlphaTest = -1
maxBeta = -1
maxBetaTest = -1

transitions = []
transitionsTest = []

def getVals (filename, flag):
    temp = []
    if flag == 1:
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
                if flag == 1:
                    counts.append(temp1)
                    lengths.append(temp2)
                temp = []
                if flag == 1:
                    temp1 = []
                    temp2 = []

            if (count == 0):
                lookupIndex = lookupIndex + 1

        temp.append(float(line))
        if flag == 1:
            temp1.append(count)
            temp2.append(len(sentences[count]))

        count = count + 1

    final.append(temp)
    if flag == 1:
        counts.append(temp1)
        lengths.append(temp2)
    f.close()
    return final

def getValsTest (filename, flag):
    temp = []
    if flag == 1:
        temp1 = []
        temp2 = []
    final = []
    lookupIndex = 0
    count = 0
    f = open(filename)
    for line in f:
        if (lookupIndex != 2560):
            if (count == transitionsTest[lookupIndex] and count != 0):
                lookupIndex = lookupIndex + 1
                final.append(temp)
                if flag == 1:
                    countsTest.append(temp1)
                    lengthsTest.append(temp2)
                temp = []
                if flag == 1:
                    temp1 = []
                    temp2 = []

            if (count == 0):
                lookupIndex = lookupIndex + 1

        temp.append(float(line))
        if flag == 1:
            temp1.append(count)
            temp2.append(len(sentencesTest[count]))

        count = count + 1

    final.append(temp)
    if flag == 1:
        countsTest.append(temp1)
        lengthsTest.append(temp2)
    f.close()
    return final

def getMaxVals(alpha, beta, lambdaVal, gamma):
    maxScores = []
    maxIndecies = []
    for i in range(0,len(stProbs)):
        maxScore = -1000000
        maxIndex = -1
        for j in range(0,len(stProbs[i])):
            score = ((1-lambdaVal) * tsProbs[i][j]) + (lambdaVal * stProbs[i][j]) + (gamma * lengths[i][j]) + (alpha * tfidf[i][j]) + (beta * glove[i][j]) 

            if score > maxScore:
                maxScore = score
                maxIndex = j
            j = j + 1
        maxScores.append(maxScore)
        maxIndecies.append(maxIndex)
        i = i + 1

    f = open("rerankedDev.txt", "w")
    startIndex = 0
    for i in range(0, len(maxIndecies)):
        f.write(sentences[counts[i][maxIndecies[i]]])
        i = i + 1
    f.close()

    perl_script = subprocess.Popen("perl multi-bleu.perl dev.tgt.txt < rerankedDev.txt > bleu.txt", shell = True)
    perl_script.communicate()
    f = open("bleu.txt")
    for line in f:
        start = line.index("=")
        end = line.index(",")
        bleu = float(line[start+2 : end])
        return bleu

def getMaxValsTest(alpha, beta, lambdaVal, gamma):
    maxScores = []
    maxIndecies = []
    for i in range(0,len(stProbsTest)):
        maxScore = -1000000
        maxIndex = -1
        for j in range(0,len(stProbsTest[i])):
            score = ((1-lambdaVal) * tsProbsTest[i][j]) + (lambdaVal * stProbsTest[i][j]) + (gamma * lengthsTest[i][j]) + (alpha * tfidfTest[i][j]) 

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
        f.write(sentencesTest[countsTest[i][maxIndecies[i]]])
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
f = open('index_dev.txt')
for line in f:
    if number != int(line):
        number = int(line)
        transitions.append(startIndex)
    startIndex = startIndex + 1
f.close()

number = 0
startIndex = 0
i = 0
f = open('index_valid.txt')
for line in f:
    if number != int(line):
        number = int(line)
        transitionsTest.append(startIndex)
    startIndex = startIndex + 1
f.close()

sentences = []
f = open('rearank_target_dev.txt')
for line in f:
    sentences.append(line)

sentencesTest = []
f = open('rearank_target_valid.txt')
for line in f:
    sentencesTest.append(line)

tsProbs = getVals('t_given_s_dev.txt', 0)
stProbs = getVals('s_given_t_dev.txt', 0)
tfidf = getVals('tfidf_dev.txt', 0)
counts = []
lengths = []
glove = getVals('dev_src_glove_dist.txt', 1)

tsProbsTest = getValsTest('t_given_s_valid.txt', 0)
stProbsTest = getValsTest('s_given_t_valid.txt', 0)
countsTest = []
lengthsTest = []
tfidfTest = getValsTest('tfidf_valid.txt', 1)
#gloveTest = getValsTest('dev_src_glove_dist.txt', 1)

for i in range(0, 10):
    alpha = random.uniform(0,0.0001)
    beta = random.uniform(-2,0)
    bleu = getMaxVals(alpha, beta, lambdaVal, gamma)
    bleuTest = getMaxValsTest(alpha, beta, lambdaVal, gamma)
    print "Alpha = " + str(alpha)
    print "Beta = " + str(beta)
    print "Dev bleu = " + str(bleu)
    print "Test bleu = " + str(bleuTest)
    if bleu > maxBleu:
        maxBleu = bleu
        maxAlpha = alpha
        maxBeta = beta

    if bleuTest > maxBleuTest:
        maxBleuTest = bleuTest
        maxAlphaTest = alpha
        maxBetaTest = beta

print "Max dev bleu = " + str(maxBleu)
print "Max test bleu = " + str(maxBleuTest)
print "Dev alpha = " + str(maxAlpha)
print "Dev beta = " + str(maxBeta)
print "Max alpha test = " + str(maxAlphaTest)
print "Max test beta = " + str(maxBetaTest)
