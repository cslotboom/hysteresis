import numpy as np
from .baseClass import Hysteresis, SimpleCycle, MonotonicCurve
from .baseFuncs import concatenateHys, _linInterpolate, _getNsamples
       
# =============================================================================
# concatenate and resample
# =============================================================================
           
def resample(curve, Nsamples):
    """
    Creates a new curve object that has a different number of sample points 
    between the start and end of each Cycle object.   
    The number of points is specified by the user, and intermediate points will
    be evenly spaced between the cycles start and end points.
    Linear interpolation is used to find the y value of intermediate points.
    In the case of a Hysteresis, every SimpleCycle curve will be resampled with
    an amount of points equal to Nsamples.

    Parameters
    ----------
    curve : Hysteresis, Monotonic Cycle, or numpy array
        The curve to be resampled
    Nsamples : 
        The number of samples for the new curve.
        
    Returns
    -------
    curve :
        An object of the input type with a number of points equal to Nsamples

    """  
        
    # We recursively resample by calling the function again for sub-cycle objects
    # if the curve is a SimpleCycle
    if isinstance(curve, SimpleCycle):
        x = curve.xy[:,0]
        y = curve.xy[:,1]
        Output = SimpleCycle(_linInterpolate(x,y, Nsamples))    
       
    # if the curve is a hysteresis, we recursively create a series of Cycles
    elif isinstance(curve, Hysteresis):
        outputCycles = [None]*curve.NCycles
        for ii, cycle in enumerate(curve.cycles):
            outputCycles[ii] = resample(cycle, Nsamples)
        Output = concatenateHys(*outputCycles)    # If curve

    # if the curve is a Monotonic Cycle
    elif isinstance(curve, MonotonicCurve):
        x = curve.xy[:,0]
        y = curve.xy[:,1]
        Output = MonotonicCurve(_linInterpolate(x,y, Nsamples))  
    
    # if it is a np array
    elif isinstance(curve, np.ndarray):
        x = curve[:,0]
        y = curve[:,1]
        Output = _linInterpolate(x,y, Nsamples)  
        
    return Output
   
def resampleDx(curve, Targetdx):
    """
    Creates a new curve object that has a different number of sample points 
    between the start and end of each Cycle object.
    For each curve, a number of points will be chosen based on some target
    displacement value in the x direction. If the value overshoots, 
    the last point will instead be used.
    For example, if the start = 2.5, end = 7.5 and dx = 2, points will be 
    placed at 2.5, 4.5, 6.5, 7.5 
    
    Linear interpolation is used to find the y value of intermediate points.
    In the case of a Hysteresis, every SimpleCycle curve will be resampled with
    an amount of points equal to Nsamples.

    Parameters
    ----------
    curve : Hysteresis, Monotonic Cycle, or numpy array
        The curve to be resampled.

    Targetdx : float
        The target distance to use for sample points.
        
    Returns
    -------
    curve :
        An object of the input type, with points approximately at Targetdx.

    """  

    if isinstance(curve, SimpleCycle):
        x = curve.xy[:,0]
        dxNet = x[-1] - x[0]
        
        Nsamples = _getNsamples(Targetdx, dxNet)
        
        Output = resample(curve, Nsamples)    
        
        
    elif isinstance(curve, Hysteresis):

        outputCycles = [None]*curve.NCycles
        for ii, Cycle in enumerate(curve.Cycles):
            outputCycles[ii] = resampleDx(Cycle, Targetdx)
        Output = concatenateHys(*outputCycles)    # If curve
       
    # if the curve is a MonotonicCurve Cycle
    elif isinstance(curve, MonotonicCurve):
    
        x = curve.xy[:,0]
        dxNet = x[-1] - x[0]
        
        Nsamples = _getNsamples(Targetdx, dxNet)
        
        Output = resample(curve, Nsamples)  
    
    # if it is a np array
    elif isinstance(curve, np.ndarray):
        x = curve[:,0]
        dxNet = x[-1] - x[0]
        
        Nsamples = _getNsamples(Targetdx, dxNet)        
        Output = resample(curve, Nsamples)
        
    return Output

