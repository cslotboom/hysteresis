import numpy as np
from .baseClass import Hysteresis, SimpleCycle, MonotonicCurve
from .baseFuncs import concatenateHys, _LinInterpolate, _getNsamples
       
# =============================================================================
# concatenate and resample
# =============================================================================
           
def resample(Curve, Nsamples):
    """
    Creates a new Curve object that has a different number of sample points 
    between the start and end of each Cycle object.   
    The number of points is specified by the user, and intermediate points will
    be evenly spaced between the cycles start and end points.
    Linear interpolation is used to find the y value of intermediate points.
    In the case of a Hysteresis, every SimpleCycle Curve will be resampled with
    an amount of points equal to Nsamples.

    Parameters
    ----------
    Curve : Hysteresis, Monotonic Cycle, or numpy array
        The curve to be resampled
    Nsamples : 
        The number of samples for the new curve.
        
    Returns
    -------
    Curve :
        An object of the input type with a number of points equal to Nsamples

    """  
        
    # We recursively resample by calling the function again for sub-cycle objects
    
    # if the curve is a SimpleCycle
    if isinstance(Curve, SimpleCycle):
    
        x = Curve.xy[:,0]
        y = Curve.xy[:,1]
        Output = SimpleCycle(_LinInterpolate(x,y, Nsamples))    
       
    # if the curve is a hysteresis, we recursively create a series of Cycles
    elif isinstance(Curve, Hysteresis):
        outputCycles = [None]*Curve.NCycles
        for ii, Cycle in enumerate(Curve.Cycles):
            outputCycles[ii] = resample(Cycle, Nsamples)
        Output = concatenateHys(*outputCycles)    # If Curve

    # if the curve is a Monotonic Cycle
    elif isinstance(Curve, MonotonicCurve):
    
        x = Curve.xy[:,0]
        y = Curve.xy[:,1]
        
        Output = MonotonicCurve(_LinInterpolate(x,y, Nsamples))  
    
    # if it is a np array
    elif isinstance(Curve, np.ndarray):
        x = Curve[:,0]
        y = Curve[:,1]
        Output = _LinInterpolate(x,y, Nsamples)  
        
    return Output
   
def resampleDx(Curve, Targetdx):
    """
    Creates a new Curve object that has a different number of sample points 
    between the start and end of each Cycle object.
    For each curve, a number of points will be chosen based on some target
    displacement value in the x direction. If the value overshoots, 
    the last point will instead be used.
    For example, if the start = 2.5, end = 7.5 and dx = 2, points will be 
    placed at 2.5, 4.5, 6.5, 7.5 
    
    Linear interpolation is used to find the y value of intermediate points.
    In the case of a Hysteresis, every SimpleCycle Curve will be resampled with
    an amount of points equal to Nsamples.

    Parameters
    ----------
    Curve : Hysteresis, Monotonic Cycle, or numpy array
        The curve to be resampled.

    Targetdx : float
        The target distance to use for sample points.
        
    Returns
    -------
    Curve :
        An object of the input type, with points approximately at Targetdx.

    """  

    if isinstance(Curve, SimpleCycle):
        x = Curve.xy[:,0]
        dxNet = x[-1] - x[0]
        
        Nsamples = _getNsamples(Targetdx, dxNet)
        
        Output = resample(Curve, Nsamples)    
        
        
    elif isinstance(Curve, Hysteresis):

        outputCycles = [None]*Curve.NCycles
        for ii, Cycle in enumerate(Curve.Cycles):
            outputCycles[ii] = resampleDx(Cycle, Targetdx)
        Output = concatenateHys(*outputCycles)    # If Curve
       
    # if the curve is a MonotonicCurve Cycle
    elif isinstance(Curve, MonotonicCurve):
    
        x = Curve.xy[:,0]
        dxNet = x[-1] - x[0]
        
        Nsamples = _getNsamples(Targetdx, dxNet)
        
        Output = resample(Curve, Nsamples)  
    
    # if it is a np array
    elif isinstance(Curve, np.ndarray):
        x = Curve[:,0]
        dxNet = x[-1] - x[0]
        
        Nsamples = _getNsamples(Targetdx, dxNet)        
        Output = resample(Curve, Nsamples)
        
    return Output

