import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math
import statsmodels.api as sm
import pylab

sp1 = np.loadtxt('servinsp1.dat')
sp2 = np.loadtxt('servinsp22.dat')
sp3 = np.loadtxt('servinsp23.dat')
ws1 = np.loadtxt('ws1.dat')
ws2 = np.loadtxt('ws2.dat')
ws3 = np.loadtxt('ws3.dat')


def drawHist(sp):
    plt.hist(sp, int(math.ceil(np.sqrt(len(sp)))), density=True)
    plt.xlabel('time(s)')
    plt.ylabel('Frequency')
    m = np.mean(sp)
    x = np.arange(0, 100, 0.1)
    y = 1/m*np.exp(-1/m*x)
    plt.plot(x, y)
    print(max(sp)/18)
    print("Expectation: "+str(np.mean(sp))+" Variance: "+str(np.var(sp)))
    plt.show()


def drawCDF(sp):
    sorted_ = np.sort(sp)
    yvals = (np.arange(len(sorted_))) / float(len(sorted_))
    plt.plot(sorted_, yvals)
    plt.xlabel('time(s)')
    plt.ylabel('Probability')
    plt.show()


def drawQ_Q(sp):
    sm.qqplot(sp, dist=stats.expon, line='r')
    pylab.show()
    # sorted_ = np.sort(sp)
    # yvals = (np.arange(len(sorted_))-1/2) / float(len(sorted_))
    # x_label = stats.expon.ppf(yvals)
    # plt.scatter(sorted_, x_label)
    # plt.xlabel('time(s)')
    # plt.ylabel('Quantile of exponential distribution')
    # plt.show()


def drawSim(sp):
    m, _ = stats.expon.fit(sp)
    sample = np.random.exponential(1/m, size=1000)
    plt.hist(sample, bins=int(math.ceil(np.sqrt(len(sp)))),
             alpha=0.7, normed=True)
    x = np.arange(0, 100, 0.1)
    y = m*np.exp(-m*x)
    plt.plot(x, y)
    plt.show()


drawHist(sp1)
drawSim(sp1)
# drawHist(ws3)
# drawHist(ws3)
# drawQ_Q(ws2)
# drawQ_Q(ws3)

# drawHist(sp2)
# drawHist(sp3)
# drawQ_Q(sp1)
