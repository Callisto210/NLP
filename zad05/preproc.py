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

def main():
    filenames = [f for f in listdir('data/') if isfile(join('data/', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    for name in filenames:
        output = open(str(re.search('\d+', name).group(0)) + '_preproc.txt', 'w')

        f = open(join('data/', name), 'r')
        judgments = json.load(f)['items']
        print(name)
        for judgment in judgments:
            try:
                if datetime.datetime.strptime(judgment['judgmentDate'], "%Y-%m-%d").year == 2005:
                    cleaned = judgment['textContent']
                    cleaned = re.sub('-\n', '', cleaned)
                    cleaned = re.sub('<[^>]*>', '', cleaned)
                    output.write(cleaned)
            except KeyError:
                pass
        f.close()
        output.close()

if __name__ == '__main__':
    sys.exit(main())
