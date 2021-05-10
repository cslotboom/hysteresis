# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt
        
disp = np.loadtxt('UFP_Disp.out',delimiter=' ')
force = np.loadtxt('UFP_RFrc.out',delimiter=' ')
testHys2 = np.column_stack([disp[:,1], -force[:,1]])
DamperHys = hys.Hysteresis(testHys2)


def test_plot_labels(monkeypatch):
    """ Tests if the cycles can plot correctly"""
    
    monkeypatch.setattr(plt, 'show', lambda: None)
    DamperHys = hys.Hysteresis(testHys2)

    DamperHys.plot(plotCycles = True, labelCycles = [17,18,19,23])
    plt.close()
    DamperHys.plot(plotCycles = True, labelCycles = 'all')
    plt.close()

    assert True == True


def test_plot_Cycles(monkeypatch):
    """ Tests if the cycles can plot correctly"""
    
    monkeypatch.setattr(plt, 'show', lambda: None)
    DamperHys = hys.Hysteresis(testHys2)

    DamperHys.plot(plotCycles = True, labelCycles = [17,18,19,23])
    plt.close()
    DamperHys.plotCycles(plotCycles = True, labelCycles = [3,6,8])
    plt.close()
    DamperHys.plotCycles([0,1])
    plt.close()

    assert True == True

def test_plot_Area(monkeypatch):
    """ Tests if the area can plot correctly."""
    
    monkeypatch.setattr(plt, 'show', lambda: None)   
    DamperHys = hys.Hysteresis(testHys2)  
    DamperHys.plotArea()

    assert True == True


def test_plot_Slope(monkeypatch):
    """ Tests if the slope can plot correctly"""
    
    monkeypatch.setattr(plt, 'show', lambda: None)   
    DamperHys = hys.Hysteresis(testHys2)  
    slope = DamperHys.slope
    DamperHys.plotSlope()
    plt.close()
    
    assert True == True


    