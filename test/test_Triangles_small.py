# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt
from  scipy.signal import sawtooth
from scipy.interpolate import interp1d

x = np.linspace(0, 1, 1000)*10
triangleSmall = sawtooth(x*20,0.5)/7
trianglexy = np.column_stack((x,triangleSmall))
smallTriangles = hys.SimpleCycle(trianglexy, findPeaks = True)





def test_plot_peaks(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    smallTriangles.setPeaks()
    smallTriangles.plot(showPeaks = True)
    plt.close()
    assert True == True


def test_plot_SubCycles(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    smallTriangles.plotSubCycles()
    plt.close()

    assert True == True


def test_plot_Slope(monkeypatch): 
    monkeypatch.setattr(plt, 'show', lambda: None)

    smallTriangles.setSlope()
    smallTriangles.plotSlope()
    plt.close()
    assert True == True

def test_Slope():
    smallTriangles.setSlope()
    slope = smallTriangles.slope
    assert abs(slope[-1] - -1.8189136353358175) < 10**-5

def test_Area():
    smallTriangles.setArea()
    Anet = smallTriangles.getNetArea()
    assert abs(Anet - 0.004982994450842999) < 10**-8





# smallTriangles.setArea()
# Anet = smallTriangles.getNetArea()
# 0.004982994450842999