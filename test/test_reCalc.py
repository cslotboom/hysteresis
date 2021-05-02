# -*- coding: utf-8 -*-
"""
Created on Sat May  1 23:49:09 2021

@author: Christian
"""


import numpy as np
import hysteresis as hys


def test_recalc_like():
    revDist =2
    revWidth = 10
    revProminence = 50
    
    
    t = np.linspace(0,1*np.pi,101)
    y = np.sin(t)
    xy = np.column_stack([t,y])
    
    
    myHys = hys.Hysteresis(xy,revDist,revWidth,revProminence)
    
    newHys = hys.Hysteresis(xy)
    
    newHys.recalculateCycles_like(myHys)
    
    
    check1 = newHys.revDist == revDist
    check2 = newHys.revWidth == revWidth
    check3 = newHys.revProminence == revProminence
    
    assert np.all([check1, check2, check3])

# print(myHys.peakProminence)

# out = myHys + t