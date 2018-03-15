import sys
from os import listdir
from os.path import isfile, join

import json
import re
import datetime
import itertools

import nltk
from bs4 import BeautifulSoup

def main():
    only_letters = re.compile(r'[\W\d]+')
    filenames = [f for f in listdir('data/') if isfile(join('data/', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    for name in filenames:
        f = open(join('data/', name), 'r')
        judgments = json.load(f)['items']
        print(name)
        for judgment in judgments:
            try:
                if datetime.datetime.strptime(judgment['judgmentDate'], "%Y-%m-%d").year == 2005:
                    cleaned = BeautifulSoup(judgment['textContent'], 'lxml').get_text()
                    tokens = nltk.tokenize.word_tokenize(cleaned)
                    wonum = list(itertools.filterfalse(only_letters.match, tokens))
                    freq = nltk.FreqDist(wonum)
                    for key, val in freq.items():
                        print (str(key) + " : " + str(val))
                    break
            except KeyError:
                pass
        f.close()
        break

if __name__ == '__main__':
    sys.exit(main())
