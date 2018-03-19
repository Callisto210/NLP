import sys
from os import listdir
from os.path import isfile, join

import json
import re
import datetime
import itertools
import csv

import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus.reader.nkjp import NKJPCorpusReader

from collections import Counter

WORDS = Counter()
N = 0

def P(word): 
    return WORDS[word] / N

def correction(word): 
    return max(candidates(word), key=P)

def candidates(word):
    cand = set([word])
    cand.update(edits1(word))
    cand.update(edits2(word))
    return (known(cand))

def known(words):
    return set(w for w in words if w in WORDS)

def edits1(word):
    letters    = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def main():
    global N
#    pl_corp = NKJPCorpusReader(root='/home/patryk/NLP/zad03/nkjp/', fileids='')
#    pl_dict = dict.fromkeys(pl_corp.words(), None)
    freqlist = []
    only_letters = re.compile(r'^[a-zA-Ząćęłńóśźż]{2,}$')

    filenames = [f for f in listdir('data/') if isfile(join('data/', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    for name in filenames:
        f = open(join('data/', name), 'r')
        judgments = json.load(f)['items']
        print(name)
        for judgment in judgments:
            try:
                if datetime.datetime.strptime(judgment['judgmentDate'], "%Y-%m-%d").year == 2005:
                    cleaned = judgment['textContent']
                    cleaned = re.sub('-\n', '', cleaned)
                    cleaned = re.sub('<[^>]*>', '', cleaned)
                    tokens = [word.lower() for word in nltk.tokenize.word_tokenize(cleaned)]
                    tokens = list(filter(only_letters.match, tokens))
                    freqlist = freqlist + tokens
                    #break
            except KeyError:
                pass
        f.close()
        #break

    freq = Counter(freqlist)
    WORDS.update(freq)
    N = sum(WORDS.values())

    for key, val in freq.most_common():
        print (str(key) + " - " + str(val))

    [w, k] = zip(*freq.most_common(30))

    plt.subplot(1,1,1)
    plt.bar(np.arange(len(w)), k, 1/1.5, log=True)
    plt.xticks(np.arange(len(w)), w, rotation='vertical')
    plt.grid(True)
    plt.show()

    polimorf = open('polimorfologik-2.1.txt')
    reader = csv.reader(polimorf, delimiter=';')
    slowar = [row[1].lower() for row in reader]

    polimorf_dict = set(slowar)

    for key, val in freq.items():
        if str(key) not in polimorf_dict:
            print (str(key) + " -> " + correction(str(key)))

if __name__ == '__main__':
    sys.exit(main())
