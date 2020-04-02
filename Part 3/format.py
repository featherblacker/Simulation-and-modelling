# -*- coding: utf-8 -*-
# @Time    : 08:31  2020/4/2  2020
# @Author  : chuqiguang
# @FileName: format.py.py
# @Software: PyCharm

import numpy as np

file = np.loadtxt('format.txt')
file = list([str(num) for num in file])
print('&'.join(file))