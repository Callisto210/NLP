import sys
from os import listdir
from os.path import isfile, join

import json
import re
import datetime
import itertools
import csv
import operator


import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus.reader.nkjp import NKJPCorpusReader

import collections
from collections import Counter, defaultdict
from math import log10, log

import xml.etree.ElementTree

def main():
    filenames = [f for f in listdir('out/') if isfile(join('out/', f)) and
                    re.match(r'judg-\d+\.ccl', f) is not None]
    res_zgr = {}
    res_zgrd = {}
    res_d = {}
    res_dr = {}
    for name in filenames:
        e = xml.etree.ElementTree.parse(join('out/', name)).getroot()
        for sentence in e.iter('sentence'):
            d = collections.defaultdict(dict)
            for tok in sentence.iter('tok'): 
                for ann in tok.iter('ann'):
                    chan = ann.get('chan')
                    nchan = ann.text
                    if int(nchan) != 0:
                        try:
                            d[chan][nchan] += ' ' + tok[0].text
                        except KeyError:
                            d[chan][nchan] = tok[0].text
            for (key, a) in d.items():
                for (_, val) in a.items():
                    try:
                        res_d[key] += 1
                    except KeyError:
                        res_d[key] = 1

                    try:
                        res_dr[(val, key)] += 1
                    except KeyError:
                        res_dr[(val, key)] = 1

    #print (res_d)
    #print (res_dr)

    for ((val, key), cnt) in res_dr.items():
        key_s = key.split('_')
        try:
            res_zgr[key_s[0]+"_"+key_s[1]].append((val, cnt))
        except KeyError:
            res_zgr[key_s[0]+"_"+key_s[1]] = [(val, cnt)]

    for (key, cnt) in res_d.items():
        key_s = key.split('_')
        try:
            res_zgrd[key_s[0]+"_"+key_s[1]] += cnt
        except KeyError:
            res_zgrd[key_s[0]+"_"+key_s[1]] = cnt

    print ('100 najcześciej występujących wyrażeń')
    top100 = sorted(res_dr.items(), key=operator.itemgetter(1), reverse=True)[:100]
    print (top100)

    print ('10 najczęściej występujących dla każdej zgrubenj kategorii')
    for k in res_zgr.keys():
        print (k)
        top10 = sorted(res_zgr[k], key=operator.itemgetter(1), reverse=True)[:10]
        print (top10)


    #Drobnoziarnista
#    xticks = list(list(zip(*res_d.items()))[0])
#    y = list(list(zip(*res_d.items()))[1])
#    x = list(range(0, len(y)))
#    plt.xticks(x, xticks, rotation=70)
#    plt.bar(x, y)
#    plt.show()


    #Bruboziarnista
#    xticks = list(list(zip(*res_zgrd.items()))[0])
#    y = list(list(zip(*res_zgrd.items()))[1])
#    x = list(range(0, len(y)))
#    plt.xticks(x, xticks, rotation=70)
#    plt.bar(x, y)
#    plt.show()


if __name__ == '__main__':
    sys.exit(main())
