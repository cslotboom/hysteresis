# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import numpy as np
import hysteresis as hys
import matplotlib.pyplot as plt


t  = np.linspace(0,4,1000)*np.pi
x  = np.sin(t)
y  = np.cos(t)*t
xy = np.column_stack([x,y])

myHys = hys.Hysteresis(xy)

# =============================================================================
# 
# =============================================================================


def test_cycles_plot(monkeypatch):
    """ Tests if the cycles can plot correctly"""
    monkeypatch.setattr(plt, 'show', lambda: None)
    myHys.cycles[0].setSubCycles()
    myHys.cycles[0].plot(showPeaks=True, showReversals=True)
    assert True == True

def test_subcycles_plot(monkeypatch):
    """ Tests if the cycles can plot correctly"""
    
    monkeypatch.setattr(plt, 'show', lambda: None)
    myHys.cycles[0].plotSubCycles(showPeaks=True)
    
    assert True == True

