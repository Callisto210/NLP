import sys
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

import ast

def main():
    for name in ['2005.out']:
#        f = open(name, 'r')
#        lines = f.readlines()
#        numbers = lines[:-3]
#        numbers = [int(float(x)) for x in numbers]
#        print numbers

        numbers = np.fromfile(open(name, 'r'), sep='\n')
        print numbers

#        v_hist = np.ravel(numbers)
#        fig = plt.figure()
#        ax1 = fig.add_subplot(111)

#        n, bins, patches = ax1.hist(v_hist, bins=50, normed=1, facecolor='green')
#        plt.show()

        fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)
        axs.hist(numbers, bins=1000, range = (1000000, 70000000000))

        plt.show()

if __name__ == '__main__':
    sys.exit(main())
