import sys
import os
import random
from collections import Counter
import numpy as np
from random import shuffle
from nltk.translate import bleu_score

hypotheses = []
references = []
transitions = []

f = open('dev.tgt_string.txt')
for line in f:
    hypothesis = line.split()
    hypotheses.append(hypothesis)
f.close()

number = 0
startIndex = 0
f = open('index_dev.txt')
for line in f:
    if number != int(line):
        number = int(line)
        transitions.append(startIndex)
    startIndex = startIndex + 1
f.close()

lookupIndex = 0
count = 0
sentences = []
f = open('rearank_target_dev.txt')
for line in f:
    if lookupIndex < len(transitions):
        if count  == transitions[lookupIndex]:
            lookupIndex = lookupIndex + 1
            sentence = [int(i) for i in line.split()]
            sentences.append(sentence)
        count = count + 1

vocab = []
f = open('movie_50000.txt')
for line in f:
    vocab.append(line.rstrip('\n'))
f.close()

stringSentences = []
for sentence in sentences:
    stringSentence = []
    for wordIndex in sentence:
        stringSentence.append(vocab[wordIndex-1])
    stringSentences.append(stringSentence)

#stringSentences = stringSentences[:1790] + stringSentences[2100:]
#hypotheses = hypotheses[:1790] + hypotheses[2100:]

stringSentencesDev = stringSentences[2000:] 
hypothesesDev = hypotheses[2000:] 

stringSentencesTest = stringSentences[2000:] 
hypothesesTest = hypotheses[2000:] 

"""
scores = []
for i,j in zip(stringSentences, hypotheses):
    references = [i]
    scores.append(bleu_score.sentence_bleu(references, j))
average = np.average(np.array(scores))
#print bleu_score.corpus_bleu(stringSentences, hypotheses)
print average
"""
print bleu_score.corpus_bleu(stringSentencesDev, hypothesesDev)
