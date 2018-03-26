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

from collections import Counter, defaultdict
from math import log10, log

all_bigrams_dict = defaultdict(lambda: defaultdict(int))
all_bigrams_dictr = defaultdict(lambda: defaultdict(int))

def h(n, v):
    if v == 0:
        return 0
    return (v/n)*log(v/n)

def calc_llr(x, n):
    ab = x[1]
    anotb = sum(all_bigrams_dict[x[0][0]].values()) - ab
    notab = sum(all_bigrams_dictr[x[0][1]].values()) - ab
    notanotb = n - (ab + anotb + notab)

    hm = h(n, ab) + h(n, anotb) + h(n, notab) + h(n, notanotb)
    hrow = h(n, ab + notab) + h(n, anotb + notanotb)
    hcol = h(n, ab + anotb) + h(n, notab + notanotb)
    return 2*n*(hm - hrow - hcol)

def main():
    all_bigrams = []
    only_letters = re.compile(r'^[a-zA-Ząćęłńóśźż]+$')

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
                    bigrams = list(zip(tokens, tokens[1:]))
                    all_bigrams = all_bigrams + bigrams
                    #break
            except KeyError:
                pass
        f.close()
        #break

    #Load unigrams
    uni = open('uni_full.txt')
    reader = csv.reader(uni, delimiter=',')
    tup = [(row[0], int(row[1])) for row in reader]
    unigrams = dict(tup)

    unigrams_n = sum(unigrams.values())

    #Create dicts
    for a, b in all_bigrams:
        all_bigrams_dict[a][b] += 1
        all_bigrams_dictr[b][a] += 1

    #Count bigrams
    bigrams_cnt = Counter(all_bigrams)
    bigrams_cnt_n = sum(bigrams_cnt.values())

    #Obtain PMI
    pmi = list(map(lambda x: (x[0], log10((x[1]/bigrams_cnt_n)/((unigrams[x[0][0]]/unigrams_n)*(unigrams[x[0][0]]/unigrams_n)))), bigrams_cnt.most_common()))

    pmi_top = sorted(pmi, key=lambda x: x[1], reverse=True)[:30]
    print (pmi_top)

    #Obtain LLR
    llr = list(map(lambda x: (x[0], calc_llr(x, bigrams_cnt_n)), bigrams_cnt.most_common()))
    llr_top = sorted(llr, key=lambda x: x[1], reverse=True)[:30]
    print (llr_top)

if __name__ == '__main__':
    sys.exit(main())
