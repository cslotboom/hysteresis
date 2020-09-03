# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.interpolate import interp1d

# a triangle with small reversals
x = np.linspace(0, 1, 1000)*10
triangleBig = scipy.signal.sawtooth(x*2,0.5)
triangleSmall = scipy.signal.sawtooth(x*20,0.5)/7
triangle = triangleBig + triangleSmall
trianglexy = np.column_stack((x,triangle))
notchedTriangles = hys.SimpleCycle(trianglexy, FindPeaks = True)

def test_notchedTriangles_peaks():
    notchedTriangles.setPeaks()
    peaks = notchedTriangles.peakIndexes

    test1 = peaks[4] == 62
    test2 = peaks[14] == 220
    test3 = peaks[31] == 486
    
    assert np.all([test1,test2,test3])

def test_notchedTriangles_Slope():
    notchedTriangles.setSlope()
    slope = notchedTriangles.Slope
   
    assert abs(slope[-1] - -0.54567409060066) < 10**-8


def test_notchedTriangles_Area():

    notchedTriangles.setArea()
    Area = notchedTriangles.getNetArea()

    assert abs(Area - -0.3595804712700046) < 10**-8

def test_notchedTriangles_recalc_peaks():
    
    notchedTriangles = hys.SimpleCycle(trianglexy, FindPeaks = True)
    notchedTriangles.recalculatePeaks(peakProminence = 0.8)
    peaks2 = notchedTriangles.peakIndexes

    assert peaks2[2] == 314