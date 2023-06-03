# -*- coding: utf-8 -*-
"""
Created on Sat May  1 23:49:09 2021

@author: Christian
"""

import numpy as np
import hysteresis as hys
from  scipy.signal import sawtooth

t = np.linspace(0,5*np.pi,1001)
y = np.sin(t)
xy = np.column_stack([t,y])

# triangleSmall = sawtooth(t *20,0.5)/7
# trianglexy = np.column_stack((triangleSmall, t))

# myHys = hys.Hysteresis(trianglexy)
# myHys.setLength()
# myHys.recalculateCycles_dist()
# myHys.plot(True)
# myHys.re

def test_recalc():
    newHys = hys.SimpleCurve(xy)
    newHys.setPeaks()
    newHys.recalculatePeaks(peakProminence=3)
    assert len(newHys.peakIndexes) == 2


def test_recalc_dist():
    
    newHys = hys.SimpleCurve(xy)
    newHys.setPeaks()
    newHys.recalculatePeaks(peakProminence=3)
    assert len(newHys.peakIndexes) == 2

def test_recalc_like():
    revDist =2
    revWidth = 10
    revProminence = 50
        
    myHys = hys.Hysteresis(xy,revDist,revWidth,revProminence)
    
    newHys = hys.Hysteresis(xy)
    
    newHys.recalculateCycles_like(myHys)
    
    
    check1 = newHys.revDist == revDist
    check2 = newHys.revWidth == revWidth
    check3 = newHys.revProminence == revProminence
    
    assert np.all([check1, check2, check3])


test_recalc_like()
# print(myHys.peakProminence)

# out = myHys + t