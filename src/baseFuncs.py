import numpy as np
from scipy.interpolate import interp1d
from .baseClass import Hysteresis, SimpleCycle, MonotonicCurve



# This is kind of unorganized right now...


# Todo:
    # make a concatenate to Cycle object.


def concatenateHys(*argv):
    """
    This function creates a new hysteresis from the xy data of a series of 
    monotonic curves, or xy curves.

    
    Parameters
    ----------
    *argv : SimpleCycle objects, or XY data
        A number of monotonic cycle objects to be combined into a hysteresis.
        These curves should be 

    Returns
    -------
    hysteresis : Hysteresis Object
        The ouput hysteresis object which is a combination of all of the input
        curves

    """
    
    # # TODO: enhance hysteresis functionality
    # I would expect that the new curve has all the propreties of the old curves.
    # Here that won't be the case, which is akward.   
    
    
    xyList = [None]*len(argv)   
           
    for ii, vector in enumerate(argv):
        # Try to read the xy data from a monotonic curve object
        try:
            tempxy = vector.xy
        except:
            tempxy = vector
            
        # for curves after the first curve, we skip the first value
        # I think we want to do this for all curves?
        if ii >= 1:
            xyList[ii] = tempxy[1:,:]
        else:
            xyList[ii] = tempxy
    
    # Create new hysteresis, then add objects to the list    
    xy = np.concatenate(xyList)
    hysteresis = Hysteresis(xy)
    
    return hysteresis


# =============================================================================
# resample functions
# =============================================================================

def _LinInterpolate(x,y, Nsamples):
    """
    A linear interpolation function that takes a target input curve to a 
    target sample curve. The sample curve goes between x0 and xN with Nsamples.
    """
    
    f = interp1d(x, y)
    
    outputx = np.linspace(x[0],x[-1], Nsamples)
    outputy = f(outputx)
    outputxy = np.column_stack((outputx, outputy))    
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