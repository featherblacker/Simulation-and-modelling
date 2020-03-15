import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math
import statsmodels.api as sm
import math
import pylab

sp1 = np.loadtxt('servinsp1.dat')
sp2 = np.loadtxt('servinsp22.dat')
sp3 = np.loadtxt('servinsp23.dat')
ws1 = np.loadtxt('ws1.dat')
ws2 = np.loadtxt('ws2.dat')
ws3 = np.loadtxt('ws3.dat')

np.random.seed(10)

def drawHist(sp):
    """Draw the histogram of the distribution of data"""
    plt.hist(sp, 20, density=True)
    plt.xlabel('time(s)')
    plt.ylabel('Frequency')
    m = np.mean(sp)
    x = np.arange(0, max(sp), 0.1)
    y = 1/m*np.exp(-1/m*x)
    plt.plot(x, y)
    print(max(sp)/18)
    print("Expectation: "+str(np.mean(sp))+" Variance: "+str(np.var(sp)))
    plt.show()


def drawCDF(sp):
    """Draw cumulative distribution function of data"""
    sorted_ = np.sort(sp)
    yvals = (np.arange(len(sorted_))) / float(len(sorted_))
    plt.plot(sorted_, yvals)
    plt.xlabel('time(s)')
    plt.ylabel('Probability')
    plt.show()


def drawQ_Q(sp):
    """Draw Quantile-Quantile plot of exponentional distribution and data"""
    sm.qqplot(sp, dist=stats.expon, line='r')
    pylab.show()
    # sorted_ = np.sort(sp)
    # yvals = (np.arange(len(sorted_))-1/2) / float(len(sorted_))
    # x_label = stats.expon.ppf(yvals)
    # plt.scatter(sorted_, x_label)
    # plt.xlabel('time(s)')
    # plt.ylabel('Quantile of exponential distribution')
    # plt.show()


def generate(sp, number):
    """Random variables generator"""
    m = np.mean(sp)
    sample = np.random.exponential(m, size=number)
    plt.hist(sample, bins=int(math.ceil(np.sqrt(len(sp)))),
             alpha=0.7)
    plt.show()
    return sample

def divide(sp, num):
    bins = [0]*num
    width = math.ceil(max(sp))//num+1
    print(width)
    for item in sp:
        bins[int(item/width)]+=1
    return bins



if __name__ == '__main__':
    # drawHist(sp1)
    # drawHist(sp2)
    # drawHist(sp3)
    # drawHist(ws1)
    # drawHist(ws2)
    # drawHist(ws3)
    # drawCDF(sp1)
    # drawCDF(sp2)
    # drawCDF(sp3)
    # drawCDF(ws1)
    # drawCDF(ws2)
    # drawCDF(ws3)
    # drawQ_Q(sp1)
    # drawQ_Q(sp2)
    # drawQ_Q(sp3)
    # drawQ_Q(ws1)
    # drawQ_Q(ws2)
    # drawQ_Q(ws3)
    generate(sp1, 300)
    generate(sp2, 300)
    generate(sp3, 300)
    generate(ws1, 300)
    generate(ws2, 300)
    generate(ws3, 300)
    # print(divide(ws1, 20))

    # RVs = drawSim(sp1, 100)
