import numpy as np
from numpy import trapz

from scipy.interpolate import interp1d
from hysteresis import data

from .data import LinearInterpolation
from .baseClass import Hysteresis, SimpleCycle
from .defaultDataFuncs import defaultAreaFunction, defaultSlopeFunction
from .defaultPlotFuncs import initializeFig, defaultPlotFunction, defaultShowCycles


import matplotlib.pyplot as plt

 




# Calculate Envelop


# lpSteps = [2]*10

# skipEnd = 0
# skipStart = 0

# =============================================================================
# Find the backbone
# =============================================================================

def _LPparser(LPsteps):
    
    # InputParser - Decides what to do with the variable LoadProtcol
    # if you get an interger use that for all cycles
    
    if len(LPsteps) ==0:
        Indexes =  []
    
    # if type(LPsteps) == int:
    else:
        # shift = LPsteps[0] - 1
        shift = 1
        Indexes = np.concatenate([[0,1], np.cumsum(LPsteps,dtype=int) + shift])
        
    return Indexes


def _getBackbonePeaks(hystersis, xyPosInd):
    
    Ncycle = len(xyPosInd)
    
    CycleIndx = xyPosInd[1:] - 1
    
    cycles = hystersis.getCycles(CycleIndx)
    peaks = np.zeros([Ncycle,2])
    for ii in range(Ncycle - 1):
        # Set the peak, then find the local index of the maximum point
        cycles[ii].setPeaks()
        tempInd = cycles[ii].maxIndexes
        
        # Get the xy coords, the aliase over the peak indexes.
        tempxy = cycles[ii].xy
        largestPeakInd = np.argmax(tempxy[tempInd,1])
        peaks[ii] = tempxy[tempInd[largestPeakInd]]

    return np.array(peaks)

"""
TODO:
    Allow for getting the peaks, end point, or both.
"""
def getBackboneCurve(hysteresis, LPsteps = [], returnPeaks = False,  
                     skipStart = 0, skipEnd =0):
    """
    Returns the positve backbone curve of a hysteresis.
        
    By default all reversal points on the backbone curve are returned.
    This will not be appropriate for some types of hysteresis where the load
    drops between cycles.
    The user can output only the first cycle of each load step by specifying 
    the number of loading cycles there are at each load step.
    By default the final point (the right most point) is returned for each
    cycle.
    The user can return the peak and final point by setting returnPeaks = True.


    Parameters
    ----------
    hysteresis : Hysteresis class
        The input Hysteresis to calculate the backbone of.
    LPsteps : list, optional
        The list of the number of cycles at each load point. The default is [].
        
        For example, if the input loading is as follows: 
        
        0, 1, -1, 1, -1, 1 , -1, 2, -2, 3,-3, 3, -3
        
        Then the input should be [3, 1, 2].
        
    returnPeaks : bool, optional
        A switch that when toggled on will cause the function to return 
        the peak points of each cycle in additon to the end points.    
    skipStart : int, optional
        The number of cycles to skip from the start of the the backbone 
        curve. The default is 0 which skips no cycles.
    skipEnd : int, optional
        The number of cycles to skip from the end of the the backbone 
        curve. The default is 0 which skips no cycles.
    Returns
    -------
    backbone : SimpleCycle
        A simpleCycle object of the output backbone curve.

    """
    
    xyPosCycle = np.array([])
    xyPosPeak = np.array([])
    
    # Get a slice of the reversal indexes
    reversalIndexes = hysteresis.reversalIndexes
    xyPoints = hysteresis.xy[reversalIndexes]
    xyPosInd = np.where(0 <= xyPoints[:,0])[0]
    
    # If it doesn't start at zero for some reason, make it start at zero.
    # We should always include the first index!
    if xyPosInd[0] != 0:
        xyPosInd = np.hstack((0,xyPosInd))
    
    Ncycle = len(xyPosInd)
    
    # mess with the indexes as necessary
    Indexes = _LPparser(LPsteps)
    if len(Indexes) != 0:
        xyPosInd = xyPosInd[Indexes]
        Ncycle = len(Indexes)
    
    # Skip any cycles that have been specified.
    endIndex = Ncycle - skipEnd
    startIndex = skipStart
    xyPosInd = xyPosInd[startIndex:endIndex]
    
    xyPosCycle = xyPoints[xyPosInd]
    xyPos = xyPosCycle
    
    # Get the postive indexes        
    if returnPeaks == True:
        xyPosPeak = _getBackbonePeaks(hysteresis, xyPosInd)
        xyPos = np.concatenate([xyPosCycle,xyPosPeak])
        
    # Remove repeated points
    xPos = xyPos[:,0]
    _, indexes = np.unique(xPos,True)
    
    xyPos = xyPos[indexes]   
    
    backbone = SimpleCycle(xyPos, True)
    
    return backbone



def getAvgBackbone(hystersis, LPsteps = [], returnPeaks = False,  
                   skipStart = 0, skipEnd =0):
    
    """
    Returns the average, positve, and negative backbone curve of a hysteresis.
        
    By default all reversal points on the backbone curve are returned.
    This will not be appropriate for some types of hysteresis where the load
    drops between cycles.
    The user can output only the first cycle of each load step by specifying 
    the number of loading cycles there are at each load step.
    By default the final point (the right most point) is returned for each
    cycle.
    The user can return the peak and final point by setting returnPeaks = True.


    Parameters
    ----------
    hysteresis : Hysteresis class
        The input Hysteresis to calculate the backbone of.
    LPsteps : list, optional
        The list of the number of cycles at each load point. The default is [].
        
        For example, if the input loading is as follows: 
        
        0, 1, -1, 1, -1, 1 , -1, 2, -2, 3,-3, 3, -3
        
        Then the input should be [3, 1, 2].
        
    returnPeaks : bool, optional
        A switch that when toggled on will cause the function to return 
        the peak points of each cycle in additon to the end points.    
    skipStart : int, optional
        The number of cycles to skip from the start of the the backbone 
        curve. The default is 0 which skips no cycles.
    skipEnd : int, optional
        The number of cycles to skip from the end of the the backbone 
        curve. The default is 0 which skips no cycles.
    Returns
    -------
    avg, pos, neg : SimpleCycle
        A simpleCycle object of the output backbone curve.

    """
    
    
    hysNeg = Hysteresis(-hystersis.xy)
    backBonePos = getBackboneCurve(hystersis, LPsteps, returnPeaks)
    backBoneNeg = getBackboneCurve(hysNeg, LPsteps, returnPeaks)
    
    xPos = backBonePos.xy[:,0]
    xNeg = backBoneNeg.xy[:,0]
    
    f1 =  interp1d(backBonePos.xy[:,0], backBonePos.xy[:,1], fill_value = 'extrapolate')
    f2 =  interp1d(backBoneNeg.xy[:,0], backBoneNeg.xy[:,1], fill_value = 'extrapolate')
    
    xnet = np.concatenate((xPos, xNeg))
    x = np.unique(xnet)
    
    ypos = f1(x)
    yneg = f2(x)
    
    yavg = (ypos + yneg) / 2
    
    xy = np.column_stack([x, yavg])
    backBoneAvg = SimpleCycle(xy)
    
    return backBoneAvg, backBonePos, backBoneNeg


def _linInterpolateY(xy, yinter, Index):
    
    """ Returns the x intercept of a target point y with a xy curve,
    Given the first index greater than the input intercept.
    
    """
    y1 = xy[Index - 1,1]
    y2 = xy[Index    ,1]
    x1 = xy[Index - 1,0]
    x2 = xy[Index    ,0]
    
    return LinearInterpolation(y1,y2,x1,x2,yinter)

# =============================================================================
# Fit EEEP
# =============================================================================

def fitEEEP(backbone):
    """
    Fits a backbone curve with a equivalent elastic perfectly plastic curve
    using the ASTM E2126 methodology.
    The cirve has equivalent area to the input backone curve.
    
    http://www.materialstandard.com/wp-content/uploads/2019/10/E2126-11.pdf

    Parameters
    ----------
    backbone : SimpleCycle
        The input SimpleCycle Object.

    Returns
    -------
    SimpleCycle
        A simpleCycle object of the backbone curve.

    """
    
    
    # There are two options - either there is a decline or there is no decline
    backbone.setArea()
    Anet = backbone.getNetArea()
    xy = backbone.xy
    
    # Ppeak = np.max(backbone.xy[:,1])
    PpeakInd = np.argmax(xy[:,1])
    xyPeak = xy[PpeakInd,:]
    Ppeak = xyPeak[1]
    dUpeak = xyPeak[0]
    
    # Find the final values of P and u 
    dUend, Pend = xy[-1,:] 
    xyFail = xy[PpeakInd:,:]
    
    # ratio = Pmax / Ppeak
    Rlim = 0.8
    Plim = Rlim*Ppeak
    
    # Find the ultimate point
    if Plim < Pend: # If the final point is greater than 0.8Ppeak, use that point.
        Pult = Pend
        dUult = dUend
    else:           # If the final point is less than 0.8Ppeak, find the intercept.
        # use linear interpolation to find the intersection point.
        Pult = Plim
        index = np.argmax(xy[:,1] < Plim)
        dUult = _linInterpolateY(xyFail, Plim, index)
    
    # Find the elastic intercept and slope.
    Pinter = 0.4*Ppeak
    index = np.argmin(xy[:,1] < Pinter)
    dUinter = _linInterpolateY(xy, Pinter, index)
    Ke = Pinter / dUinter
    
    
    radicand = dUult**2 - 2*Anet/Ke
    
    if 0 < radicand:
        Py = Ke*(dUult - (radicand)**0.5)
    else:
        Py = 0.85*Ppeak
    
    curve = np.column_stack([[0, Py/Ke, dUult], [0,Py,Py]])
    
    return SimpleCycle(curve)



