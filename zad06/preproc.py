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
    groups = [
        ('AC', re.compile(r'A?C.*'),''),
        ('AU', re.compile(r'A?U.*'),''),
        ('AK', re.compile(r'A?K.*'),''),
        ('G', re.compile(r'G.*'),''),
        ('AP', re.compile(r'A?P.*'),''),
        ('R', re.compile(r'R.*'),''),
        ('W', re.compile(r'W.*'),''),
        ('Am', re.compile(r'Am.*'),'')]
    filenames = [f for f in listdir('data/') if isfile(join('data/', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    for name in filenames:
        f = open(join('data/', name), 'r')
        judgments = json.load(f)['items']
        print(name)
        for judgment in judgments:
            try:
                if datetime.datetime.strptime(judgment['judgmentDate'], "%Y-%m-%d").year == 2005 and
                  judgement['courtType'] in ['COMMON', 'SUPREME']:
                    cleaned = judgment['textContent']
                    cleaned = re.sub('-\n', '', cleaned)
                    cleaned = re.sub('<[^>]*>', '', cleaned)
                    casenum = judgment['courtCases']['caseNumber']
                    for _, r, s in groups:
                        if r.match(casenum) is not None:
                            s = s + cleaned
                            break
            except KeyError:
                pass
        f.close()

    for n, _, s in groups:
        o = open(join(n, '.txt'), 'w')
        o.write(requests.post('localhost:8081', data=s.encode('utf-8')).content)
        o.close()

if __name__ == '__main__':
    sys.exit(main())
