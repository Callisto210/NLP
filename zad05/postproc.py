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

    pairs = []
    f = open('tags.txt', 'r')
    for line in f:
        if line.startswith('\t'):
            if 'interp' not in line:
                w, t, *_ = line.split()
                cat = t.split(':')[0]
                pairs.append((w.lower() + ":" + cat))

    all_bigrams = list(zip(pairs, pairs[1:]))

    f.close()

    #Create dicts
    for a, b in all_bigrams:
        all_bigrams_dict[a][b] += 1
        all_bigrams_dictr[b][a] += 1

    #Count bigrams
    bigrams_cnt = Counter(all_bigrams)
    bigrams_cnt_n = sum(bigrams_cnt.values())

    #print(bigrams_cnt.most_common(30))

    #Obtain LLR
    llr = list(map(lambda x: (x[0], calc_llr(x, bigrams_cnt_n)), bigrams_cnt.most_common()))
    llr_noun = list(filter(lambda x: re.match('.*?:subst', x[0][0]) != None and 
        re.match('.*?:subst|.*?:adj', x[0][1]) != None, llr))
    llr_top = sorted(llr_noun, key=lambda x: x[1], reverse=True)[:30]
    print (llr_top)

if __name__ == '__main__':
    sys.exit(main())
