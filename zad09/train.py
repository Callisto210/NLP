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

def main():

    input = LineSentence('cleaned_judgments2')
    bigram = Phrases(input)
    trigram = Phrases(bigram[input])
    model = Word2Vec(trigram[bigram[input]], sg=0, size=300, window=5, min_count=3, workers=8)
    model.save('model2')

if __name__ == '__main__':
    sys.exit(main())
