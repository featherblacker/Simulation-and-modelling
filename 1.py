import numpy as np

sp = np.loadtxt('ws1.dat')
print(sp)
summation = 0
for item in sp:
    summation+=item
print(summation)