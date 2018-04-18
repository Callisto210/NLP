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

import requests
import pickle

def main():
    only_letters = re.compile(r'[^a-zA-ZąĄćĆęĘłŁńŃóÓśŚźŹżŻ \n]+')
    top_words = re.compile(r'\b(art|do|na|nie|że|przez|dnia|się|sąd|jest|ust|ustawy|od|sądu|to|oraz|prawa|za|nr|tym)\b', re.IGNORECASE)
    groups = [
        ['AC', re.compile(r'A?C.*'), [], [], 0, True],
        ['AU', re.compile(r'A?U.*'), [], [], 0, True],
        ['AK', re.compile(r'A?K.*'), [], [], 0, True],
        ['G', re.compile(r'G.*'), [], [], 0, True],
        ['AP', re.compile(r'A?P.*'), [], [], 0, True],
        ['R', re.compile(r'R.*'), [], [], 0, True],
        ['W', re.compile(r'W.*'), [], [], 0, True],
        ['Am', re.compile(r'Am.*'), [], [], 0, True]]

    sum_of_judgments = 0
    filenames = [f for f in listdir('data/') if isfile(join('data/', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    for year in range(2005, 2017):
        print("Year: " + str(year))
        for name in filenames:
            f = open(join('data/', name), 'r')
            judgments = json.load(f)['items']
            #print(name)
            for judgment in judgments:
                try:
                    if datetime.datetime.strptime(judgment['judgmentDate'], "%Y-%m-%d").year in [year] and judgment['courtType'] in ['COMMON', 'SUPREME']:
                        cleaned = judgment['textContent']
                        cleaned = re.sub('-\n', '', cleaned)
                        cleaned = re.sub('<[^>]*>', '', cleaned)
                        justification = re.search(r'(U|u) ?(Z|z) ?(A|a) ?(S|s) ?(A|a) ?(D|d) ?(N|n) ?(I|i) ?(E|e) ?(N|n) ?(I|i) ?(E|e).*', cleaned)
                        if justification is not None:
                            sum_of_judgments += 1
                            cleaned = cleaned[justification.start() : ]
                            cleaned = only_letters.sub('', cleaned)
                            cleaned = top_words.sub('', cleaned)
                            for cas in judgment['courtCases']:
                                casenum = str(cas['caseNumber'])
                                for group in groups:
                                    if group[1].search(casenum) is not None and group[5] == True:
                                        group[2].append(cleaned)
                                        group[4] += 1
                                        break
                except KeyError:
                    pass
            f.close()
        ok = True
        for group in groups:
            print(group[0] + ": " + str(group[4]))
            if group[4] < 100:
                ok = False
            else:
                group[5] = False

        if ok == True:
            break

    print("All judgments: " + str(sum_of_judgments))
    for group in groups:
        print (str(group[0]) + " judgments: " + str(group[4]))
        for s in group[2]:
            group[3].append(requests.post('http://localhost:9200', data=s.encode('utf-8')).content.decode('utf-8'))

    o = open('dump', 'wb')
    o.write(pickle.dumps(groups))
    o.close()

if __name__ == '__main__':
    sys.exit(main())
