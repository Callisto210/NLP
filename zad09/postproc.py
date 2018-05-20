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

from gensim.models import Word2Vec, Phrases
from gensim.models.word2vec import LineSentence
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

st = ['Sąd_Najwyższy',
      'Trybunał_Konstytucyjny',
      'kodeks_cywilny',
      'kpk',
      'sąd_rejonowy',
      'szkoda',
      'wypadek',
      'kolizja',
      'szkoda_majątkowa',
      'nieszczęście',
      'rozwód']

rd = ['szkoda',
      'strata',
      'uszczerbek',
      'szkoda_majątkowa',
#      'uszczerbek_na_zdrowiu',
      'krzywda',
      'niesprawiedliwość',
      'nieszczęście']


def main():

    model = Word2Vec.load('model')
    for w in st:
        print(w + ": " + str(model.wv.most_similar(w)[:3]))
    
    print('\n')
    print ("Sąd Najwyższy - kpc + konstytucja: " + str(model.wv.most_similar(positive=['Sąd_Najwyższy', 'konstytucja'], negative=['kpc'])[:5]))
    print ("pasażer - mężczyzna + kobieta: " + str(model.wv.most_similar(positive=['pasażer', 'kobieta'], negative=['mężczyzna'])[:5]))
    print ("samochód - droga + rzeka: " + str(model.wv.most_similar(positive=['samochód', 'rzeka'], negative=['droga'])[:5]))

    X = model[rd]

    tsne = TSNE(n_components=2)
    X_tsne = tsne.fit_transform(X)

    plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
    plt.show()

if __name__ == '__main__':
    sys.exit(main())
