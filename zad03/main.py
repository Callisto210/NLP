import sys
from os import listdir
from os.path import isfile, join

import json
import re
import datetime

import nltk

def main():
    filenames = [f for f in listdir('data/') if isfile(join('data/json', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    for name in filenames:
        f = open(join('data/json', name), 'r')
        judgments = json.load(f)['items']
        for judgment in judgments:
            try:
                if datetime.datetime.strptime(judgment['judgmentDate'], "%Y-%m-%d").year == 2005:
                    cleaned = nltk.clean_html(judgment['textContent'])
                    tokens = nltk.word_tokenize(cleaned)
                    print(tokens)
            except KeyError:
                pass
        f.close()
        break

if __name__ == '__main__':
    sys.exit(main())
