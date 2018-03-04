import sys
from os import listdir
from os.path import isfile, join

import json
import re
import datetime

def find_money(s):
#    print("------------------------")
#    res = re.findall('((?:\d+(?:\\\\n|[\.\s])*)+)(?:,\s*?(\d+))?(?:\\\\n|\s)*(?:zł|PLN|złotych)(?:(?:\\\\n|\s)*(\d{2})(?:\\\\n|\s)*(?:gr|groszy))?(?:\\\\n|[\s\W])+', s)
#    print(res)

    res = re.findall('(?:((?:\d+(?:\\\\n|[\.\s])*)+)(?:,\s*?(\d+))?(?:\\\\n|\s)*bi(?:\\\\n|-)*lion(?:ów|y)?(?:\\\\n|\s)*)?'
        '(?:((?:\d+(?:\\\\n|[\.\s])*)+)(?:,\s*?(\d+))?(?:\\\\n|\s)*mi(?:\\\\n|-)*liard(?:ów|y)?(?:\\\\n|\s)*)?'
        '(?:((?:\d+(?:\\\\n|[\.\s])*)+)(?:,\s*?(\d+))?(?:\\\\n|\s)*mi(?:\\\\n|-)*lion(?:ów|y)?(?:\\\\n|\s)*)?'
        '(?:((?:\d+(?:\\\\n|[\.\s])*)+)(?:,\s*?(\d+))?(?:\\\\n|\s)*ty(?:\\\\n|-)*si(?:ąc|ące|ęcy)?(?:\\\\n|\s)*)?'
        '(?:sta(?:\\\\n|-)*rych)?(?:\\\\n|\s)*(?:zł(?:(?:\\\\n|-)*otych)?|PLN)(?:\\\\n|[\s\W])+', s)
    print(res)

def count_judgment(judgments):
    #Bill from 23.04.1964 has journalNo 16
    try:
        for regulation in judgment['referencedRegulations']:
            if regulation['journalNo'] == 16 and regulation['journalYear'] == 1964:
                if re.search('art\. 445', regulation['text']) is not None:
                    print(regulation['text'])
    except KeyError:
        pass

def count_harm(s):
    res = re.findall(r'\b(?:(?:szkod(?:a|y|zie|ę|ą|o|om|ami|ach))|szkód)\b', s)
    print(res)

def main():
    filenames = [f for f in listdir('data/json') if isfile(join('data/json', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
#    for name in filenames:
    for name in ['judgments-3006.json']:
        print(name)
        f = open(join('data/json', name), 'r')
        judgments = json.load(f)['items']
        for judgment in judgments:
            try:
#                if datetime.datetime.strptime(judgment['judgmentDate'], "%Y-%m-%d").year == 2016:
#                    print(judgment['judgmentDate'])
    #            count_harm(str(judgment))
                find_money(str(judgment))
        #        count_judgment(judgment)
        #        print(str(judgment))
            except KeyError:
                pass
        f.close()
#        break
        

if __name__ == '__main__':
    sys.exit(main())
