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
    filenames = [f for f in listdir('data/') if isfile(join('data/', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    d = {}
    train = {}
    test = {}
    limit = 20000
    for name in filenames:
        if limit == 0:
            break
        limit = limit - 1
        f = open(join('data/', name), 'r')
        section = None
        judgments = json.load(f)['items']
        for judgment in judgments:
            for judges in judgment['judges']:
                if 'REPORTING_JUDGE' in judges['specialRoles']:
                    section = judges['name']
                    break

            if section == None:
                break

            section = re.sub(' ', '_', section)

            body = judgment['textContent']
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

    train_res = []

    for (category, texts) in d.items():
        if len(texts) < 500:
            continue
        print (category + str(len(texts)))
        random.shuffle(texts)
        for text in texts[:int((len(texts)+1)*.75)]:
            train_res.append('\n__label__' + category + ' ' + text)
        for text in texts[int((len(texts))*.75+1):]:
            test_file.write('\n__label__' + category + ' ' + text)

    random.shuffle(train_res)
    for text in train_res:
        train_file.write(text)

    train_file.close()
    test_file.close()

if __name__ == '__main__':
    sys.exit(main())
