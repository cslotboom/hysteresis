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

x = np.linspace(0, 1, 1000)*10
triangleSmall = scipy.signal.sawtooth(x*20,0.5)/10
triangleBig = scipy.signal.sawtooth(x,0.5)
triangle = triangleSmall + triangleBig
Y = x**2


def test_plot_RemoveNeg(monkeypatch):
    """ Tests if the remove Negative attribute runs"""
    
    monkeypatch.setattr(plt, 'show', lambda: None)
    

    trianglexy = np.column_stack((triangle,Y))
    smallTriangles = hys.Hysteresis(trianglexy)
    smallTriangles.recalculateCycles(peakProminence=.2)
    
    cycle1 = smallTriangles.getCycle(0)
    
    xy = cycle1.xy
    x = xy[:,0]
    y = xy[:,1]
    
    direction = cycle1.direction
    difference = np.append(0, np.diff(x))
    
    condtion = np.where(0 <= difference*direction)
    
    plt.subplots()
    plt.plot(x[condtion], y[condtion])
    
    New = hys.removeNegative(cycle1)
    New.plot()

    assert True == True