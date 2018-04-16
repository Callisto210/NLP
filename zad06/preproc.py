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

def main():
    only_letters = re.compile(r'[^a-zA-ZąĄćĆęĘłŁńŃóÓśŚźŹżŻ \n]+')
    groups = [
        ['AC', re.compile(r'A?C.*'),''],
        ['AU', re.compile(r'A?U.*'),''],
        ['AK', re.compile(r'A?K.*'),''],
        ['G', re.compile(r'G.*'),''],
        ['AP', re.compile(r'A?P.*'),''],
        ['R', re.compile(r'R.*'),''],
        ['W', re.compile(r'W.*'),''],
        ['Am', re.compile(r'Am.*'),'']]
    filenames = [f for f in listdir('data/') if isfile(join('data/', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    for name in filenames:
        f = open(join('data/', name), 'r')
        judgments = json.load(f)['items']
        print(name)
        for judgment in judgments:
            try:
                if datetime.datetime.strptime(judgment['judgmentDate'], "%Y-%m-%d").year == 2005 and judgment['courtType'] in ['COMMON', 'SUPREME']:
                    cleaned = judgment['textContent']
                    cleaned = re.sub('-\n', '', cleaned)
                    cleaned = re.sub('<[^>]*>', '', cleaned)
                    justification = re.search('U ?z ?a ?s ?a ?d ?n ?i ?e ?n ?i ?e.*', cleaned)
                    if justification is not None:
                        cleaned = cleaned[justification.start() : ]
                        cleaned = only_letters.sub('', cleaned)
                        casenum = str(judgment['courtCases'][0]['caseNumber'])
                        for group in groups:
                            if group[1].search(casenum) is not None:
                                group[2] += cleaned
                                break
            except KeyError:
                pass
        f.close()

    for n, _, s in groups:
        print (n)
        o = open(n + '.txt', 'w')
        o.write(requests.post('http://localhost:9200', data=s.encode('utf-8')).content.decode('utf-8'))
        o.close()

if __name__ == '__main__':
    sys.exit(main())
