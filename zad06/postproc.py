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
import pickle
import random

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.metrics import average_precision_score
from sklearn.metrics import confusion_matrix

def get_words(lem):
    norm = []
    basic = []
    for line in lem.split('\n'):
        if line != '':
            w, *_ = line.split()
            if line.startswith('\t') == False:
                norm.append(w)
            else:
                basic.append(w)
    return (norm, basic)

def main():
#    groups = [
#        ['AC', re.compile(r'A?C.*'), [], [], 0, True],
#        ['AU', re.compile(r'A?U.*'), [], [], 0, True],
#        ['AK', re.compile(r'A?K.*'), [], [], 0, True],
#        ['G', re.compile(r'G.*'), [], [], 0, True],
#        ['AP', re.compile(r'A?P.*'), [], [], 0, True],
#        ['R', re.compile(r'R.*'), [], [], 0, True],
#        ['W', re.compile(r'W.*'), [], [], 0, True],
#        ['Am', re.compile(r'Am.*'), [], [], 0, True]]

    o = open('dump', 'rb')
    groups = pickle.Unpickler(o).load()
    o.close()

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', OneVsRestClassifier(LinearSVC()))
    ])
    parameters = {
        'tfidf__max_df': (0.25, 0.5, 0.75),
        'tfidf__ngram_range': [(1, 1), (1, 2), (1, 3)],
        "clf__estimator__C": [0.01, 0.1, 1],
        "clf__estimator__class_weight": ['balanced', None],
    }

#[0] - Declined classifier, [1] - Basic classifier, [2] - number of words
    classifiers = {
        'AC': [GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1),
            GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1), 0],
        'AU': [GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1),
            GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1), 0],
        'AK': [GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1),
            GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1), 0],
        'G': [GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1),
            GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1), 0],
        'AP': [GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1),
            GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1), 0],
        'R': [GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1),
            GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1), 0],
        'W': [GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1),
            GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1), 0],
        'Am': [GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1),
            GridSearchCV(pipeline, parameters, cv=2, n_jobs=8, verbose=1), 0]
    }

    #List of tuple (judgment, group)
    train_all_normal = []
    test_all_normal = []
    train_all_basic = []
    test_all_basic = []

    for group in groups:
        print (group[0] + ' judgments: ' + str(group[4]))
        judgments_lem = group[3]
        random.shuffle(judgments_lem)
        train = judgments_lem[:int((len(judgments_lem)+1)*.75)]
        test = judgments_lem[int((len(judgments_lem))*.75+1):]

        for lem in train:
            (n, b) = get_words(lem)
            classifiers[group[0]][2] += len(n)
            train_all_normal += list(map(lambda x: (x, group[0]), n))
            train_all_basic += list(map(lambda x: (x, group[0]), b))
        
        for lem in test:
            (n, b) = get_words(lem)
            test_all_normal += list(map(lambda x: (x, group[0]), n))
            test_all_basic += list(map(lambda x: (x, group[0]), b))

    print('Training:')
    for k, c in classifiers.items():
        print ('Group: ' + k + ' Declined forms')
        [train_x, train_y] = zip(*train_all_normal)
        train_x = list(train_x)
        train_y = list(map(lambda x: True if x == k else False, list(train_y)))
        c[0].fit(train_x, train_y)

        print ('Group: ' + k + ' Basic forms')
        [train_x, train_y] = zip(*train_all_basic)
        train_x = list(train_x)
        train_y = list(map(lambda x: True if x == k else False, list(train_y)))
        c[1].fit(train_x, train_y)

    dec = [0, 0, 0, 0, 0]
    bas = [0, 0, 0, 0, 0]

    print('Testing:')
    for k, c in classifiers.items():
        [test_x, test_y] = zip(*test_all_normal)
        test_x = list(test_x)
        test_y = list(map(lambda x: True if x == k else False, list(test_y)))
        best = c[0].best_estimator_
        predict = best.predict(test_x)
        print ('Group: ' + k + ' Declined forms')
        print ('Words: ' + str(c[2]))
        tn, fp, fn, tp = confusion_matrix(test_y, predict).ravel()
        prec = tp/(tp+fp)
        rec = tp/(tp+fn)
        f1 = (2*prec*rec)/(prec+rec)
        dec[0] += tp
        dec[1] += tp + fp
        dec[2] += tp + fn
        dec[3] += prec
        dec[4] += rec
        print ('TP: ' + str(tp) + ' TN: ' + str(tn) + ' FP: ' + str(fp) + ' FN: ' + str(fn))
        print ('Precision: ' + str(prec) + ' Recall: ' + str(rec) + ' F1: ' + str(f1))

        print (classification_report(test_y, predict))

        [test_x, test_y] = zip(*test_all_basic)
        test_x = list(test_x)
        test_y = list(map(lambda x: True if x == k else False, list(test_y)))
        best = c[1].best_estimator_
        predict = best.predict(test_x)
        print ('Group: ' + k + ' Basic forms')
        print ('Words: ' + str(c[2]))
        tn, fp, fn, tp = confusion_matrix(test_y, predict).ravel()
        prec = tp/(tp+fp)
        rec = tp/(tp+fn)
        f1 = (2*prec*rec)/(prec+rec)
        bas[0] += tp
        bas[1] += tp + fp
        bas[2] += tp + fn
        bas[3] += prec
        bas[4] += rec
        print ('TP: ' + str(tp) + ' TN: ' + str(tn) + ' FP: ' + str(fp) + ' FN: ' + str(fn))
        print ('Precision: ' + str(prec) + ' Recall: ' + str(rec) + ' F1: ' + str(f1))

        print (classification_report(test_y, predict))

    print ('Declined forms:')
    prec = dec[0]/dec[1]
    rec = dec[0]/dec[2]
    f1 = (2*prec*rec)/(prec+rec)
    print ('MICRO: Precision: ' + str(prec) + ' Recall: ' + str(rec) + ' F1: ' + str(f1))

    prec = dec[3]/8
    rec = dec[4]/8
    f1 = (2*prec*rec)/(prec+rec)
    print ('MACRO: Precision: ' + str(prec) + ' Recall: ' + str(rec) + ' F1: ' + str(f1))

    print ('Basic forms:')
    prec = bas[0]/bas[1]
    rec = bas[0]/bas[2]
    f1 = (2*prec*rec)/(prec+rec)
    print ('MICRO: Precision: ' + str(prec) + ' Recall: ' + str(rec) + ' F1: ' + str(f1))

    prec = bas[3]/8
    rec = bas[4]/8
    f1 = (2*prec*rec)/(prec+rec)
    print ('MACRO: Precision: ' + str(prec) + ' Recall: ' + str(rec) + ' F1: ' + str(f1))

if __name__ == '__main__':
    sys.exit(main())
