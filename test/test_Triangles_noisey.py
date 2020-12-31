# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt
import scipy



# a noisey triangle signal
np.random.seed(101)
x = np.linspace(0, 1, 1000)*10
triangleBig = scipy.signal.sawtooth(x*2,0.5)
permutate = np.random.normal(0,1,1000)/2
Ynoise = triangleBig + permutate
Ynoise = scipy.signal.savgol_filter(Ynoise,53,2)
trianglexy = np.column_stack((x, Ynoise))


def test_noisey_triangles():
    noiseyTriangles = hys.SimpleCycle(trianglexy, FindPeaks = True)
    noiseyTriangles.recalculatePeaks(peakWidth = 100)
    peak2 = noiseyTriangles.peakIndexes
    noiseyTriangles.plot(plotPeaks = True)
    
    test1 = len(peak2) == 7
    test2 = peak2[-2] == 794
    assert np.all([test1, test2])
    
    
def test_noisey_triangle_Area():
    noiseyTriangles = hys.SimpleCycle(trianglexy, FindPeaks = True)
    noiseyTriangles.setArea()
    area = noiseyTriangles.getNetArea()

    assert (area - -0.22793618247762648) < 10**-5