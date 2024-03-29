# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:13:13 2019
@author: Christian
"""
import numpy as np
import hysteresis as hys
from hysteresis.envelope import _LPparser
from scipy.signal import savgol_filter
import pytest

# =============================================================================
# Load initial stuff
# =============================================================================

data = np.loadtxt('Trial2.csv', skiprows = 2, delimiter  =',')
x = data[:,0]
x = savgol_filter(x,15,1)
y = data[:,1]
xy = np.column_stack([x,y])
lp = [5,3,3,3,3,3,3,3,3]
myHys = hys.Hysteresis(xy)


Lp2 = [6,6,6,4,2,2,2,2,2]

# =============================================================================
# Find the backbone
# =============================================================================

def test_lpsteps_Nstep():
    parse = _LPparser(lp)
    solution = np.array([0,1,6,9,12,15,18,21,24,27])
    
    diff = np.sum(np.abs(solution- parse))
    
    assert len(parse) == (len(lp)+1)
    assert diff < 10**-6


def test_lpsteps_Nstep2():
    parse = _LPparser(Lp2)
    solution = np.array([0,1,7,13,19,23,25,27,29,31])
    
    diff = np.sum(np.abs(solution- parse))
    
    assert len(parse) == (len(Lp2)+1)
    assert diff < 10**-6


def test_inputParse():
    """makes sure we get an error if the user doesn't ask for one of end points
    or peaks."""
    # Function: get envelope curve
    analHys = hys.Hysteresis(xy)
    # analHys.plotVsIndex(True)
    
    with pytest.raises(ValueError) as errorInfo:
    
        # Get the backbone
        backbone = hys.getBackboneCurve(analHys, lp, False, False)
        # assert True

    assert errorInfo.type is ValueError


def test_backbone():
    # Function: get envelope curve
    analHys = hys.Hysteresis(xy)
    
    # Get the backbone
    hys.getBackboneCurve(analHys, lp, True)
    hys.getBackboneCurve(analHys, lp, True,includeNegative=True)

    assert True == True

# =============================================================================
# Fit the backbone curve.
# =============================================================================

def test_fit_avg():
    
    avg, pos, neg = hys.getAvgBackbone(myHys, lp, True, True)   
    avg.setArea()
    avg.plot()
    A1 = avg.getNetArea()
    
    Curve = hys.fitEEEP(avg)
    Curve.setArea()
    A2 = Curve.getNetArea()
    
    check1 = abs(A1 - 6622.37) < 0.01
    check2 = abs(A2 - 5775.33) < 0.01
    # check2 = (A1 - A2) < 10**-6
    assert np.all((check1, check2))



def test_negative_BB():
    backbone = hys.getBackboneCurve(myHys, lp,1,1, includeNegative=True)
    
    xyReversal = myHys.getReversalxy()
    
    finalPos = xyReversal[-3]
    finalNeg = xyReversal[-2]
    
    xy = backbone.xy
    
    posDiff = sum(np.abs(finalPos - xy[-1]))
    negDiff = sum(np.abs(finalNeg - xy[0]))
    
    assert posDiff < 0.01 and negDiff < 0.01


def ManualTest():
    """
    lets us visually inspect if anything seems wrong
    """
    avg, pos, neg = hys.getAvgBackbone(myHys, lp)   
    backbone = hys.getBackboneCurve(myHys, lp,1,1, includeNegative=True)

    
    fig, ax = myHys.initFig()
    myHys.plot()
    backbone.plot()
    # neg.plot()

if __name__ == '__main__':
    ManualTest()

    test_lpsteps_Nstep()
    test_lpsteps_Nstep2()
    test_inputParse()
    test_backbone()
    test_fit_avg()
    test_negative_BB()


