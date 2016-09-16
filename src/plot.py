#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import string
from collections import Counter


X = list( string.digits + string.ascii_lowercase )


class Plot():
    def __init__(self,stat,name):
        self.s = stat
        self.l = len(name)
        self.n = name
        print(self.n)

    def draw(self):
        row = 5  #np.int_(len(self.l))
        col = 36 #np.int_(len(X))
        a = np.zeros(shape = (row,col) )
        axes = []
        for l in range(self.l):
           # print("X --> {}".format(X))
            data = dict(self.s[l])
    #        print(sorted(data.items()))
            arr = np.zeros(len(X))
            for x in X:
                i = X.index(x)
                if x in data:
                    arr[i] = data[x]
           #         print("x={}: --> {}".format(x,data[x]))
            a[l] = arr/sum(arr)
        
        colors = ['r','g','b','m','c']
        N = len(X)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.1      # the width of the bars
        fig, ax = plt.subplots()
        
        for l in range(self.l):
            print(a[l])

            axes.append(ax.bar(ind + (width*l), a[l], width, color=colors[l]))
            ax.set_xticks(ind + width)
            ax.set_xticklabels(X)
        
        ax.legend(axes, self.n)

        plt.show()
