import sys
import os
import time
import glob
from os import listdir
from os.path import isfile, join

import json
import re
import datetime
import itertools
import csv

def main():
    bytes = 0
    output = open('cleaned_judgments2', 'w')
    filenames = [f for f in listdir('data/') if isfile(join('data/', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    for name in filenames:
        f = open(join('data/', name), 'r')
        judgments = json.load(f)['items']
        print(name)
        for judgment in judgments:
            if bytes >= 4*1024*1024*1024:
                break
            try:
                cleaned = judgment['textContent']
                cleaned = re.sub('-\n', '', cleaned)
                cleaned = re.sub('<[^>]*>', '', cleaned)
                output.write(cleaned)
                bytes += len(cleaned)
            except KeyError:
                pass
        if bytes >= 4*1024*1024*1024:
            break
        f.close()

if __name__ == '__main__':
    sys.exit(main())
