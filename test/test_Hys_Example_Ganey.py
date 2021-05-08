# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt
import hysteresis.Animate.core as ani
        
disp = np.loadtxt('UFP_Disp.out',delimiter=' ')
force = np.loadtxt('UFP_RFrc.out',delimiter=' ')
testHys2 = np.column_stack([disp[:,1], -force[:,1]])

DamperHys = hys.Hysteresis(testHys2) 
DamperHys.plot(True)

viewer = ani.CycleViewer(DamperHys)
# ani.CycleViewer(DamperHys)
# viewer.updateplt(0)
# viewer.updateplt(0)

def test_plot_Slope():
    """ Tests if the slope is the correct value"""

    DamperHys = hys.Hysteresis(testHys2)  
    slope = DamperHys.Slope
    
    assert abs(slope[-2] - 40499.99999999157) < 10**-5
    

    
def test_net_Area():
    """ Tests if the net area is correct."""
    
    DamperHys = hys.Hysteresis(testHys2)
    NetArea = DamperHys.getNetArea()

    assert abs(NetArea - 12390.79659964981) < 10**-5

    
def test_reversalIndexes():
    """ Tests if the reversalIndexe is correct."""
    
    DamperHys = hys.Hysteresis(testHys2)
    reversalIndexes = DamperHys.reversalIndexes
    
    assert reversalIndexes[15] == 492
    