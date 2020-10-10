# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis.hys as hys
import numpy as np
import matplotlib.pyplot as plt
        
disp = np.loadtxt('UFP_Disp.out',delimiter=' ')
force = np.loadtxt('UFP_RFrc.out',delimiter=' ')
testHys2 = np.column_stack([disp[:,1], -force[:,1]])

def test_DownSampled_Plotting(monkeypatch):
    """ Tests if the resampled hystresis can plot correctly """
    
    monkeypatch.setattr(plt, 'show', lambda: None)
    DamperHys = hys.Hysteresis(testHys2)
    
    downsampledHys = hys.reSample(DamperHys, 20)
    downsampledHys.plot(plotCycles = True)
    plt.close()
    downsampledHys.plotCycles([2,3])
    plt.close()
    downsampledHys.plotArea()
    plt.close()
    downsampledHys.plotSlope()    
    plt.close()
    
    assert True == True


