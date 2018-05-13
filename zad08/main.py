import sys
import os
import time
import glob
import urllib2
from os import listdir
from os.path import isfile, join

import json
import re
import datetime
import itertools
import csv

url="http://ws.clarin-pl.eu/nlprest2/base" 
user="paduda@student.agh.edu.pl" 
lpmn="any2txt|wcrft2|liner2({\"model\":\"n82\"})"


def process(data):
        doc=json.dumps(data)
        taskid = urllib2.urlopen(urllib2.Request(url+'/startTask/',doc,{'Content-Type': 'application/json'})).read()
        time.sleep(0.2)
        resp = urllib2.urlopen(urllib2.Request(url+'/getStatus/'+taskid))
        data=json.load(resp)
        while data["status"] == "QUEUE" or data["status"] == "PROCESSING" :
            time.sleep(0.5)
            resp = urllib2.urlopen(urllib2.Request(url+'/getStatus/'+taskid))
            data=json.load(resp)
        if data["status"]=="ERROR":
            print("Error "+data["value"])
            return None
        return data["value"]

def clarinIt(doc, name):
    out_path= 'out/'

    fileid=urllib2.urlopen(urllib2.Request(url+'/upload/',doc.encode('utf-8'),{'Content-Type': 'binary/octet-stream'})).read()
    data={'lpmn':lpmn,'user':user,'file':fileid}
    data=process(data)
    if data == None:
        return
    data=data[0]["fileID"]
    content = urllib2.urlopen(urllib2.Request(url+'/download'+data)).read()

    with open (out_path+os.path.basename(name)+'.ccl', "w") as outfile:
            outfile.write(content)

def main():
    njudgments = 0
    filenames = [f for f in ['judgments-98.json', 'judgments-99.json'] if isfile(join('data/', f)) and
                    re.match(r'judgments-\d+\.json', f) is not None]
    for name in filenames:
        f = open(join('data/', name), 'r')
        judgments = json.load(f)['items']
        print(name)
        for judgment in judgments:
            if njudgments >= 100:
                break
            try:
                if datetime.datetime.strptime(judgment['judgmentDate'], "%Y-%m-%d").year == 2005:
                    cleaned = judgment['textContent']
                    cleaned = re.sub('-\n', '', cleaned)
                    cleaned = re.sub('<[^>]*>', '', cleaned)
                    clarinIt(cleaned, 'judg-' + str(njudgments))
                    njudgments += 1
            except KeyError:
                pass
        if njudgments >= 100:
            break
        f.close()

if __name__ == '__main__':
    sys.exit(main())
