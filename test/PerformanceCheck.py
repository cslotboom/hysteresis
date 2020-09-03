# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian

This tests if a simple cicle works
"""



import openseespytools.hystersis as hys
import numpy as np


import time

basePoints = np.linspace(0,1,1000)*2*np.pi
testCirclex = np.sin(basePoints)
testCircley = np.cos(basePoints)
Circlexy = np.column_stack((testCirclex, testCircley))

NStep = 10000

t1 = time.time()
for ii in range(NStep):
    pass

t2 = time.time()



t3 = time.time()
for ii in range(NStep):
    Circle = hys.Hystersis(Circlexy)

t4 = time.time()

dt1 = t2- t1
dt2 = t4- t3
print(dt1, dt2, dt2 - dt1)


        


