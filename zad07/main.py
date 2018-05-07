import sys
from os import listdir
from os.path import isfile, join
import os

import json
import re
import datetime
import itertools
import csv


import requests
import pickle

import WNQuery
import SemFeatures

import networkx as nx
import matplotlib.pyplot as plt

wnpath = 'plwordnet_3_1/plwordnet-3.1-visdisc.xml'
wnpath2 = 'plwordnet_3_1/plwordnet-3.1.xml'

relations = ["hypernym", "hyponym",
    "holo_member", "mero_member",
    "holo_part", "mero_part",
    "holo_portion", "mero_portion",
    "region_domain", "region_member",
    "usage_domain", "usage_member",
    "category_domain", "category_member",
    "near_antonym",
    "middle",
    "verb_group",
    "similar_to",
    "also_see",
    "be_in_state",
    "eng_derivative",
    "is_consequent_state_of", "has_consequent_state",
    "is_preparatory_phase_of", "has_preparatory_phase",
    "is_telos_of", "has_telos",
    "subevent", "has_subevent",
    "causes", "caused_by"]

group1 = [
    ('szkoda', 2),
    ('strata', 1),
    ('uszczerbek', 1),
    ('szkoda majątkowa', 1),
    ('uszczerbek na zdrowiu', 1),
    ('krzywda', 1),
    ('niesprawiedliwość', 1),
    ('nieszczęście', 2)]

group2 = [
    ('wypadek', 1),
    ('wypadek komunikacyjny', 1),
    ('kolizja', 2),
    ('zderzenie', 2),
    ('kolizja drogowa', 1),
#    ('bezkolizyjny', 2),
    ('katastrofa budowlana', 1),
    ('wypadek drogowy', 1)]

def write_synset(syns, out):
    buff = []
    for i in syns.synonyms:
        buff.append("{0}:{1}".format(i.literal, i.sense))
    print("{0}  {{{1}}}  ({2})".format(syns.wnid, ", ".join(buff), syns.definition), file=out)

def write_synset_id(wn, wnid, pos, out):
    syns = wn.lookUpID(wnid, pos)
    if syns:
        write_synset(syns, out)

def print_literal(wn, word, out):
    res = [item for i in ["a", "v", "n", "b"] for item in wn.lookUpLiteral(word, i)]

    if not res:
        print("Literal not found\n", file=out)
    else:
        for i in res:
            write_synset(i, out)
    print("", file=out)

def trace(wn, word, k, out):
    senses = wn.lookUpLiteral(word, k)
    if not senses:
        print("Literal not found\n", file=out)
    else:
        for i in senses:
            oss = wn.traceRelationOS(i.wnid, k, 'hypernym')
            if not oss:
                print("Synset not found\n", file=out)
            else:
                print("\n".join(oss), end="\n\n", file=out)

def hiperonimy(wn, word, out):
    for k in ["n", "v", "a", "b"]:
        res = wn.lookUpLiteral(word, k)
        if not res:
            continue
        else:
            j = res[0]
            write_synset_id(wn, j.wnid, k, out)
            ids = wn.lookUpRelation(j.wnid, k, 'hypernym')
            if ids:
                for i in ids:
                    print("  ", end="", file=out)
                    write_synset_id(wn, i, k, out)
        print("", file=out)

def hiponimy(wn, word, sense, out):
    for k in ["n"]:
        res = wn.lookUpLiteral(word, k)
        if not res:
            continue
        else:
            for j in res:
                if sense >= 0:
                    found = False
                    for l in wn.lookUpID(j.wnid, k).synonyms:
                        if l.sense == str(sense) and l.literal == word:
                            found = True
                    if found == False:
                       continue; 
                write_synset_id(wn, j.wnid, k, out)
                ids = wn.lookUpRelation(j.wnid, k, 'hyponym')
                if ids:
                    for i in ids:
                        print("  ", end="", file=out)
                        write_synset_id(wn, i, k, out)
                        ids2 = wn.lookUpRelation(i, k, 'hyponym')
                        if ids2:
                            for ii in ids2:
                                print("      ", end="", file=out)
                                write_synset_id(wn, ii, k, out)
        print("", file=out)

def getSemanticRelations(wn, g, k):
    res = []
    for i in g:
        for j in g:
            for relation in ['hypernym']:
                fw = wn.lookUpSense(i[0], i[1], k)
                sw = wn.lookUpSense(j[0], j[1], k)
                lur = wn.lookUpRelation(fw.wnid, k, relation)
                #print (str(i) + " " + str(j) + " " + relation + str(lur))
                if sw.wnid in lur:
                    res.append((str(i[0])+":"+str(i[1]), str(j[0])+":"+str(j[1]), {'label':relation}))
    return(res)

def similarityLeacockChodorowHacked(wn, wnid1, wnid2, pos):
    results = dict()
    for relation in relations:
        results[wn.simLeaCho(wnid1, wnid2, pos, relation, 1)] = (wnid1, wnid2, relation)
    return results

def getSimilarity(wn, w1, s1, w2, s2, pos):
    fw = wn.lookUpSense(w1, s1, pos)
    sw = wn.lookUpSense(w2, s2, pos)
    return similarityLeacockChodorowHacked(wn, fw.wnid, sw.wnid, pos)

def drawGraph(rel):
    g1 = nx.DiGraph()
    g1.add_edges_from(rel)
    nx.draw_networkx(g1, pos=nx.shell_layout(g1))
    nx.draw_networkx_edge_labels(g1, pos=nx.shell_layout(g1), font_size=7)
    plt.axis('off')
    plt.show()


def main():
    word = 'szkoda'

    print("Reading XML...", file=sys.stderr)
    wn = WNQuery.WNQuery(wnpath, open(os.devnull, "w"))
    wn.writeStats(sys.stderr)

    print_literal(wn, word, sys.stdout)
#    hiperonimy(wn, 'wypadek drogowy', sys.stdout)
    trace(wn, 'wypadek drogowy', 'n', sys.stdout)
#    trace(wn, 'nieszczęście', 'n', sys.stdout)
#    trace(wn, 'katastrofa budowlana', 'n', sys.stdout)


    toDraw = [('wypadek drogowy', 'wypadek komunikacyjny'),
                ('wypadek komunikacyjny', 'wypadek'),
                ('wypadek', 'zdarzenie oceniane negatywnie'),
                ('zdarzenie oceniane negatywnie', 'wydarzenie')]
    drawGraph(toDraw)

    print ("")
    print ('Hiponimy \"wypadek\"')
    hiponimy(wn, 'wypadek', 1, sys.stdout)

    rel = getSemanticRelations(wn, group1, 'n')
    drawGraph(rel)

    rel2 = getSemanticRelations(wn, group2, 'n')
    drawGraph(rel2)

    print (getSimilarity(wn, 'szkoda', 2, 'wypadek', 1, 'n'))
    print (getSimilarity(wn, 'kolizja', 2, 'szkoda majątkowa', 1, 'n'))
    print (getSimilarity(wn, 'nieszczęście', 2, 'katastrofa budowlana', 1, 'n'))

if __name__ == '__main__':
    sys.exit(main())
