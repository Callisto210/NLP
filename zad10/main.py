import sys
from os import listdir
from os.path import isfile, join

import json
import re
import datetime
import itertools
import csv
import operator
import random


import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus.reader.nkjp import NKJPCorpusReader

import collections
from collections import Counter, defaultdict
from math import log10, log

import xml.etree.ElementTree

def main():
    filenames = [f for f in listdir('dane/data/') if isfile(join('dane/data/', f)) and
                    re.match(r'\d+\.xml', f) is not None]
    d = {}
    train = {}
    test = {}
    for name in filenames:
        e = xml.etree.ElementTree.parse(join('dane/data/', name)).getroot()
        section = e[2].text
        section = re.sub(' ', '_', section)
        body = e[4].text
        body = re.sub('-\n', '', body)
        body = re.sub('\n', ' ', body)
        body = re.sub('<[^>]*>', '', body)
        body = body.lower()

        try:
            d[section].append(body)
        except KeyError:
            d[section] = [body]
            
    train_file = open('train.txt', 'w')
    test_file = open('test.txt', 'w')

    for (category, texts) in d.items():
        print (category + str(len(texts)))
        random.shuffle(texts)
        for text in texts[:int((len(texts)+1)*.75)]:
            train_file.write('\n__label__' + category + ' ' + text)
        for text in texts[int((len(texts))*.75+1):]:
            test_file.write('\n__label__' + category + ' ' + text)

    train_file.close()
    test_file.close()

if __name__ == '__main__':
    sys.exit(main())
