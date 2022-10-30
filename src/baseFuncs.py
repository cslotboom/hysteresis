import numpy as np
from scipy.interpolate import interp1d
from .baseClass import Hysteresis, SimpleCycle, MonotonicCurve



# This is kind of unorganized right now...


# Todo:
    # make a concatenate to Cycle object.

def concatenate(curves, outputClass = Hysteresis):
    """
    This function creates a new curve from the xy data of a series of 
    curves, or xy arrays.
    
    The output object is new - if curves are used in the concatenation, 
    propreties from those curves, i.e. peaks, revesral points, etc, will 
    not be included in the output curve.
    
    If the last point of one curve is the first point of the next point, 
    that point will be skipped.

    Parameters
    ----------
    curves : list of curves
        A number of curves, or numpy arrays. Curves must a have a xy attribute
        numpy arrays must be 2D

    Returns
    -------
    hysteresis : Hysteresis Object
        The ouput hysteresis object which is a combination of all of the input
        curves

    """  
    
    
    xyList = [None]*len(curves)   
    for ii, vector in enumerate(curves):
        # Try to read the xy data from a monotonic curve object
        try:
            tempxy = vector.xy
        except:
            tempxy = vector
            
        # for curves after the first curve, we skip the first value
        if ii >= 1 and np.all(xyList[ii-1][-1] - vector[0] == 0):
            xyList[ii] = tempxy[1:,:]
        else:
            xyList[ii] = tempxy
    
    # Create new hysteresis, then add objects to the list    
    xy = np.concatenate(xyList)
    output = outputClass(xy)
    return output


def concatenateHys(curves):
    """
    This function creates a new hysteresis from the xy data of a series of 
    monotonic curves, or xy curves.
    
    If curves are used in the concatenation, propreties from those curves 
    will be lost.

    Parameters
    ----------
    argv : SimpleCycle objects, or XY data
        A number of monotonic cycle objects to be combined into a hysteresis.
        These curves should be 

    Returns
    -------
    hysteresis : Hysteresis Object
        The ouput hysteresis object which is a combination of all of the input
        curves

    """
    return concatenate(curves)


# =============================================================================
# resample functions
# =============================================================================

def _linInterp(x,y, Nsamples):
    """
    A linear interpolation function that takes a target input curve to a 
    target sample curve. The sample curve goes between x0 and xN with Nsamples.
    """
    
    f = interp1d(x, y)
    
    outputx = np.linspace(x[0],x[-1], Nsamples)
    outputy = f(outputx)
    outputxy = np.column_stack((outputx, outputy))    
    return outputxy

def _linInterpSample(x,y, xSamples):
    """
    A linear interpolation function that takes a target input curve to a 
    target sample curve. Output of the curve are given at each sample point 
    """
    
    f = interp1d(x, y)
    
    outputy = f(xSamples)
    outputxy = np.column_stack((xSamples, outputy))    
    return outputxy


def _getNsamples(Targetdx, dxNet):
    if Targetdx >= abs(dxNet/2):
        print('Targetdx is larger than dxNet/2, no intermediate points made for the target dx = ' +str(dxNet))
        Nsamples = 2
    else:
        Nsamples = int(round(abs(dxNet/Targetdx))) + 1
    return Nsamples



# =============================================================================
# Tools for creating a load protocol
# =============================================================================

def _RemoveNeg(x, y, direction):
    
    difference = np.append(0, np.diff(x))
    
    condition = np.where(0 <= difference*direction)
    
    xOut = x[condition]
    yOut = y[condition]
    
    xy = np.column_stack([xOut, yOut])
    
    return xy

def removeNegative(Curve):
    """
    Removed values where the curve moves

    Parameters
    ----------
    Curve : TYPE
        DESCRIPTION.

    Returns
    -------
    Output : TYPE
        DESCRIPTION.

    """
    
    """
    Removes intermitent negative values in a simple curve.
    """
    
    
    # Get sample parameters, then pass those to the new curve.
    
    # if the curve is a SimpleCycle
    if isinstance(Curve, SimpleCycle):
    
        x = Curve.xy[:,0]
        y = Curve.xy[:,1]
        direction = Curve.direction
        Output = SimpleCycle(_RemoveNeg(x, y, direction))    
       
    # if the curve is a hysteresis, we recursively create a series of Cycles
    elif isinstance(Curve, Hysteresis):
        outputCycles = [None]*Curve.NCycles
        for ii, Cycle in enumerate(Curve.Cycles):
            outputCycles[ii] = removeNegative(Cycle)
        Output = concatenateHys(*outputCycles)    # If Curve

    # if the curve is a Monotonic Cycle
    elif isinstance(Curve, MonotonicCurve):
    
        x = Curve.xy[:,0]
        y = Curve.xy[:,1]
        direction = Curve.direction
        
        print('Monotonic curves should have no reversals...')
        Output = MonotonicCurve(_RemoveNeg(x, y, direction))  
    
    # if it is a np array
    elif isinstance(Curve, np.ndarray):
        x = Curve[:,0]
        y = Curve[:,1]
        
        # TODO: Create a standardized get direction function
        if x[0] <= x[-1]:
            direction = 1
        else:
            direction = -1
        
        Output = _RemoveNeg(x, y, direction)

    return  Output




# def get

