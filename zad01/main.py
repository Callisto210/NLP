import sys
from os import listdir
from os.path import isfile, join

import json
import re
import datetime

def find_money(s):
    l = []
    res = re.findall('((?:\d+(?:\\\\n|[\.\s])*)+)(?:,\s*?(\d+))?(?:\\\\n|\s)*'
        '(?:sta(?:\\\\n|-)*rych)?(?:\\\\n|\s)*(?:zł(?:(?:\\\\n|-)*otych)?|PLN)(?:(?:\\\\n|\s)*(\d{2})(?:\\\\n|\s)*(?:gr|gro(?:\\\\n|-)*szy))?(?:\\\\n|[\s\W])+', s)
    for (c, u, g) in res:
        c = re.sub("[^0-9]", "", c)
        u = re.sub("[^0-9]", "", u)
        g = re.sub("[^0-9]", "", g)
        if c == '': c = '0'
        if u == '': u = '0'
        if g == '': g = '0'
        n = int(c) + (int(u) + int(g))/100
        print(n)

    res = re.findall('(?:((?:\d+(?:\\\\n|[\.\s])*)+)(?:,\s*?(\d+))?(?:\\\\n|\s)*bi(?:\\\\n|-)*lion(?:ów|y)?(?:\\\\n|\s)*)?'
        '(?:((?:\d+(?:\\\\n|[\.\s])*)+)(?:,\s*?(\d+))?(?:\\\\n|\s)*mi(?:\\\\n|-)*liard(?:ów|y)?(?:\\\\n|\s)*)?'
        '(?:((?:\d+(?:\\\\n|[\.\s])*)+)(?:,\s*?(\d+))?(?:\\\\n|\s)*mi(?:\\\\n|-)*lion(?:ów|y)?(?:\\\\n|\s)*)?'
        '(?:((?:\d+(?:\\\\n|[\.\s])*)+)(?:,\s*?(\d+))?(?:\\\\n|\s)*ty(?:\\\\n|-)*si(?:ąc|ące|ęcy)?(?:\\\\n|\s)*)?'
        '(?:sta(?:\\\\n|-)*rych)?(?:\\\\n|\s)*(?:zł(?:(?:\\\\n|-)*otych)?|PLN)(?:\\\\n|[\s\W])+', s)
    for (bln, ubln, mld, umld, mln, umln, tys, utys) in res:
        bln = re.sub("[^0-9]", "", bln)
        ubln = re.sub("[^0-9]", "", ubln)
        if bln == '': bln = '0'
        if ubln == '': ubln = '0'
        mld = re.sub("[^0-9]", "", mld)
        umld = re.sub("[^0-9]", "", umld)
        if mld == '': mld = '0'
        if umld == '': umld = '0'
        mln = re.sub("[^0-9]", "", mln)
        umln = re.sub("[^0-9]", "", umln)
        if mln == '': mln = '0'
        if umln == '': umln = '0'
        tys = re.sub("[^0-9]", "", tys)
        utys = re.sub("[^0-9]", "", utys)
        if tys == '': tys = '0'
        if utys == '': utys = '0'
        n = 1000000000000 * int(bln) + 1000000000 * (int(ubln)+int(mld)) + 1000000 * (int(umld)+int(mln)) + 1000 * (int(umln)+int(tys)) + int(utys)
        if n != 0:
            print(n)

def count_judgment(judgment):
    #Bill from 23.04.1964 has journalNo 16
    try:
        for regulation in judgment['referencedRegulations']:
            if regulation['journalNo'] == 16 and regulation['journalYear'] == 1964:
                if re.search('art\. 445', regulation['text']) is not None:
                    return True
                return False
    except KeyError:
        pass

def count_harm(s):
    if re.search(r'\b(?:(?:szkod(?:a|y|zie|ę|ą|o|om|ami|ach))|szkód)\b', s) is not None:
        return True
    return False

def main():
    harm = 0
    judg = 0
    cnt = 0
    filenames = [f for f in listdir('data/json') if isfile(join('data/json', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    for name in filenames:
#        print(name)
        f = open(join('data/json', name), 'r')
        judgments = json.load(f)['items']
        for judgment in judgments:
            try:
                if datetime.datetime.strptime(judgment['judgmentDate'], "%Y-%m-%d").year == 2016:
                    cnt = cnt + 1
                    if count_harm(str(judgment)) == True:
                        harm = harm + 1
                    if count_judgment(judgment) == True:
                        judg = judg + 1
                    find_money(str(judgment))
            except KeyError:
                pass
        f.close()
#        break
    print("Ilość orzeczeń " + str(cnt))
    print("Ilość orzeczeń ze słowem \"szkoda\" " + str(harm))
    print("Ilość orzeczeń odwołujących się " + str(judg))
        

if __name__ == '__main__':
    sys.exit(main())
