import numpy as np
from .baseClass import Hysteresis, SimpleCycle, MonotonicCurve
from .baseFuncs import concatenateHys, _LinInterpolate, _getNsamples
       
# =============================================================================
# concatenate and resample
# =============================================================================
           
def resample(Curve, Nsamples):
    """
    Creates a new Hysteresis or Monotonic Curve object that has a different 
    number of sample points between the start and end of each Cycle object. 
    
    Linear interpolation is used for intermediate points

    Parameters
    ----------
    Curve : Hysteresis, Monotonic Cycle, or numpy array
        The curve to be resampled

    Nsamples : 
        The number of samples
        
    Returns
    -------
    TYPE
        An object of the input type.

    """  
        
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

    Parameters
    ----------
    Curve : TYPE
        DESCRIPTION.
    Targetdx : TYPE
        DESCRIPTION.

    Returns
    -------
    Output : TYPE
        DESCRIPTION.

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

