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


# def test_plot_Slope():
""" Tests if the slope is the correct value"""
def test_cum_Disp():
    DamperHys = hys.Hysteresis(testHys2)  
    
    LP = DamperHys.loadProtocol
    # The total area contained by the hystresis, including end cycles
    cumDisp = DamperHys.getNetCumDisp()
    LPcumDisp = np.sum(np.abs(LP[:-2]))*2 + LP[-2] + (LP[-2] - LP[-1])
    
    assert abs((cumDisp - LPcumDisp)) < 10**-8

    
