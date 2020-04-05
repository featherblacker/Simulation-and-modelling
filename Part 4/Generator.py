# -*- coding: utf-8 -*-
# @Time    : 20:10  2020/3/15  2020
# @Author  : chuqiguang
# @FileName: Part 2.py.py
# @Software: PyCharm

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math
import statsmodels.api as sm
import math
import pylab

sp1 = np.loadtxt('./real data/servinsp1.dat')
sp2 = np.loadtxt('./real data/servinsp22.dat')
sp3 = np.loadtxt('./real data/servinsp23.dat')
ws1 = np.loadtxt('./real data/ws1.dat')
ws2 = np.loadtxt('./real data/ws2.dat')
ws3 = np.loadtxt('./real data/ws3.dat')

np.random.seed(11)


def generate(sp, number, name):
    """Random variables generator"""
    m = np.mean(sp)
    sample = np.random.exponential(m, size=number)
    stack = []
    for item in sample:
        stack.append('{:.2f}'.format(item))
    with open("./Replication 5/{}.txt".format(name), 'w') as file:
        file.write(" ".join(stack))
    plt.hist(sample, bins=int(math.ceil(np.sqrt(len(sp)))),
             alpha=0.7)
    # plt.show()
    return sample


if __name__ == '__main__':
    generate(ws3, 300, 'ws3')
    generate(ws2, 300, 'ws2')
    generate(ws1, 300, 'ws1')
    generate(sp3, 300, 'sp3')
    generate(sp2, 300, 'sp2')
    generate(sp1, 300, 'sp1')
