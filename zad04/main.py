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
from math import log10

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
                    break
            except KeyError:
                pass
        f.close()
        break

    #Load unigrams
    uni = open('uni_full.txt')
    reader = csv.reader(uni, delimiter=',')
    tup = [(row[0], int(row[1])) for row in reader]
    unigrams = dict(tup)

    unigrams_n = sum(unigrams.values())

    #Count bigrams
    bigrams_cnt = Counter(all_bigrams)
    bigrams_cnt_n = sum(bigrams_cnt.values())

    #Obtain PMI
    pmi = list(map(lambda x: (x[0], log10((x[1]/bigrams_cnt_n)/((unigrams[x[0][0]]/unigrams_n)*(unigrams[x[0][0]]/unigrams_n)))), bigrams_cnt.most_common()))

    pmi_top = sorted(pmi, key=lambda x: x[1], reverse=True)[:30]
    print (pmi_top)


if __name__ == '__main__':
    sys.exit(main())
