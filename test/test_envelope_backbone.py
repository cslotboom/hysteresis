# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:13:13 2019
@author: Christian
"""
import numpy as np
import hysteresis as hys
from scipy.signal import savgol_filter


# =============================================================================
# Load initial stuff
# =============================================================================

data = np.loadtxt('Trial2.csv', skiprows = 2, delimiter  =',')
x = data[:,0]
x = savgol_filter(x,15,1)
y = data[:,1]
xy = np.column_stack([x,y])
lp = [5,3,3,3,3,3,3,3]
myHys = hys.Hysteresis(xy)



# =============================================================================
# Find the backbone
# =============================================================================

def test_backbone():
    # Function: get envelope curve
    analHys = hys.Hysteresis(xy)
    # analHys.plotVsIndex(True)
    
    # Get the backbone
    backbone = hys.getBackboneCurve(analHys, lp, 1)

    assert True == True



# =============================================================================
# Fit the backbone curve.
# =============================================================================

def test_fit_avg():
    avg, pos, neg = hys.getAvgBackbone(myHys, lp, 1)   
    avg.setArea()
    A1 = avg.getNetArea()
    
    Curve = hys.fitEEEP(avg)
    Curve.setArea()
    A2 = Curve.getNetArea()
    
    check1 = abs(A1 - 6622.37) < 0.01
    check2 = (A1 - A2) < 10**-6
    assert np.all((check1, check2))
